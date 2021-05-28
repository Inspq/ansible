"""High level functions for working with containers."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import atexit
import contextlib
import json
import random
import time
import uuid

from . import types as t

from .encoding import (
    Text,
)

from .util import (
    ApplicationError,
    SubprocessError,
    display,
    get_host_ip,
    sanitize_host_name,
)

from .util_common import (
    named_temporary_file,
)

from .config import (
    EnvironmentConfig,
    IntegrationConfig,
    WindowsIntegrationConfig,
)

from .docker_util import (
    ContainerNotFoundError,
    DockerInspect,
    docker_exec,
    docker_inspect,
    docker_pull,
    docker_rm,
    docker_run,
    docker_start,
    get_docker_command,
    get_docker_container_id,
    get_docker_host_ip,
)

from .ansible_util import (
    run_playbook,
)

from .core_ci import (
    SshKey,
)

from .target import (
    IntegrationTarget,
)

from .ssh import (
    SshConnectionDetail,
    SshProcess,
    create_ssh_port_forwards,
    create_ssh_port_redirects,
    generate_ssh_inventory,
)

# information about support containers provisioned by the current ansible-test instance
support_containers = {}  # type: t.Dict[str, ContainerDescriptor]


class HostType:
    """Enum representing the types of hosts involved in running tests."""
    origin = 'origin'
    control = 'control'
    managed = 'managed'


def run_support_container(
        args,  # type: EnvironmentConfig
        context,  # type: str
        image,  # type: str
        name,  # type: name
        ports,  # type: t.List[int]
        aliases=None,  # type: t.Optional[t.List[str]]
        start=True,  # type: bool
        allow_existing=False,  # type: bool
        cleanup=None,  # type: t.Optional[bool]
        cmd=None,  # type: t.Optional[t.List[str]]
        env=None,  # type: t.Optional[t.Dict[str, str]]
):  # type: (...) -> ContainerDescriptor
    """
    Start a container used to support tests, but not run them.
    Containers created this way will be accessible from tests.
    """
    if name in support_containers:
        raise Exception('Container already defined: %s' % name)

    # SSH is required for publishing ports, as well as modifying the hosts file.
    # Initializing the SSH key here makes sure it is available for use after delegation.
    SshKey(args)

    aliases = aliases or [sanitize_host_name(name)]

    current_container_id = get_docker_container_id()

    publish_ports = True
    docker_command = get_docker_command().command

    if docker_command == 'docker':
        if args.docker:
            publish_ports = False  # publishing ports is not needed when test hosts are on the docker network

        if current_container_id:
            publish_ports = False  # publishing ports is pointless if already running in a docker container

    options = ['--name', name]

    if start:
        options.append('-d')

    if publish_ports:
        for port in ports:
            options.extend(['-p', str(port)])

    if env:
        for key, value in env.items():
            options.extend(['--env', '%s=%s' % (key, value)])

    support_container_id = None

    if allow_existing:
        try:
            container = docker_inspect(args, name)
        except ContainerNotFoundError:
            container = None

        if container:
            support_container_id = container.id

            if not container.running:
                display.info('Ignoring existing "%s" container which is not running.' % name, verbosity=1)
                support_container_id = None
            elif not container.image:
                display.info('Ignoring existing "%s" container which has the wrong image.' % name, verbosity=1)
                support_container_id = None
            elif publish_ports and not all(port and len(port) == 1 for port in [container.get_tcp_port(port) for port in ports]):
                display.info('Ignoring existing "%s" container which does not have the required published ports.' % name, verbosity=1)
                support_container_id = None

            if not support_container_id:
                docker_rm(args, name)

    if support_container_id:
        display.info('Using existing "%s" container.' % name)
        running = True
        existing = True
    else:
        display.info('Starting new "%s" container.' % name)
        docker_pull(args, image)
        support_container_id = docker_run(args, image, options, create_only=not start, cmd=cmd)
        running = start
        existing = False

    if cleanup is None:
        cleanup = not existing

    descriptor = ContainerDescriptor(
        image,
        context,
        name,
        support_container_id,
        ports,
        aliases,
        publish_ports,
        running,
        existing,
        cleanup,
        env,
    )

    if not support_containers:
        atexit.register(cleanup_containers, args)

    support_containers[name] = descriptor

    return descriptor


def get_container_database(args):  # type: (EnvironmentConfig) -> ContainerDatabase
    """Return the current container database, creating it as needed, or returning the one provided on the command line through delegation."""
    if not args.containers:
        args.containers = create_container_database(args)
    elif isinstance(args.containers, (str, bytes, Text)):
        args.containers = ContainerDatabase.from_dict(json.loads(args.containers))

    display.info('>>> Container Database\n%s' % json.dumps(args.containers.to_dict(), indent=4, sort_keys=True), verbosity=3)

    return args.containers


class ContainerAccess:
    """Information needed for one test host to access a single container supporting tests."""
    def __init__(self, host_ip, names, ports, forwards):  # type: (str, t.List[str], t.Optional[t.List[int]], t.Optional[t.Dict[int, int]]) -> None
        # if forwards is set
        #   this is where forwards are sent (it is the host that provides an indirect connection to the containers on alternate ports)
        #   /etc/hosts uses 127.0.0.1 (since port redirection will be used)
        # else
        #   this is what goes into /etc/hosts (it is the container's direct IP)
        self.host_ip = host_ip

        # primary name + any aliases -- these go into the hosts file and reference the appropriate ip for the origin/control/managed host
        self.names = names

        # ports available (set if forwards is not set)
        self.ports = ports

        # port redirections to create through host_ip -- if not set, no port redirections will be used
        self.forwards = forwards

    def port_map(self):  # type: () -> t.List[t.Tuple[int, int]]
        """Return a port map for accessing this container."""
        if self.forwards:
            ports = list(self.forwards.items())
        else:
            ports = [(port, port) for port in self.ports]

        return ports

    @staticmethod
    def from_dict(data):  # type: (t.Dict[str, t.Any]) -> ContainerAccess
        """Return a ContainerAccess instance from the given dict."""
        forwards = data.get('forwards')

        if forwards:
            forwards = dict((int(key), value) for key, value in forwards.items())

        return ContainerAccess(
            host_ip=data['host_ip'],
            names=data['names'],
            ports=data.get('ports'),
            forwards=forwards,
        )

    def to_dict(self):  # type: () -> t.Dict[str, t.Any]
        """Return a dict of the current instance."""
        value = dict(
            host_ip=self.host_ip,
            names=self.names,
        )

        if self.ports:
            value.update(ports=self.ports)

        if self.forwards:
            value.update(forwards=self.forwards)

        return value


class ContainerDatabase:
    """Database of running containers used to support tests."""
    def __init__(self, data):  # type: (t.Dict[str, t.Dict[str, t.Dict[str, ContainerAccess]]]) -> None
        self.data = data

    @staticmethod
    def from_dict(data):  # type: (t.Dict[str, t.Any]) -> ContainerDatabase
        """Return a ContainerDatabase instance from the given dict."""
        return ContainerDatabase(dict((access_name,
                                       dict((context_name,
                                             dict((container_name, ContainerAccess.from_dict(container))
                                                  for container_name, container in containers.items()))
                                            for context_name, containers in contexts.items()))
                                      for access_name, contexts in data.items()))

    def to_dict(self):  # type: () -> t.Dict[str, t.Any]
        """Return a dict of the current instance."""
        return dict((access_name,
                     dict((context_name,
                           dict((container_name, container.to_dict())
                                for container_name, container in containers.items()))
                          for context_name, containers in contexts.items()))
                    for access_name, contexts in self.data.items())


def local_ssh(args):  # type: (EnvironmentConfig) -> SshConnectionDetail
    """Return SSH connection details for localhost, connecting as root to the default SSH port."""
    return SshConnectionDetail('localhost', 'localhost', None, 'root', SshKey(args).key, args.python_executable)


def create_container_database(args):  # type: (EnvironmentConfig) -> ContainerDatabase
    """Create and return a container database with information necessary for all test hosts to make use of relevant support containers."""
    origin = {}  # type: t.Dict[str, t.Dict[str, ContainerAccess]]
    control = {}  # type: t.Dict[str, t.Dict[str, ContainerAccess]]
    managed = {}  # type: t.Dict[str, t.Dict[str, ContainerAccess]]

    for name, container in support_containers.items():
        if container.details.published_ports:
            published_access = ContainerAccess(
                host_ip=get_docker_host_ip(),
                names=container.aliases,
                ports=None,
                forwards=dict((port, published_port) for port, published_port in container.details.published_ports.items()),
            )
        else:
            published_access = None  # no published access without published ports (ports are only published if needed)

        if container.details.container_ip:
            # docker containers, and rootfull podman containers should have a container IP address
            container_access = ContainerAccess(
                host_ip=container.details.container_ip,
                names=container.aliases,
                ports=container.ports,
                forwards=None,
            )
        elif get_docker_command().command == 'podman':
            # published ports for rootless podman containers should be accessible from the host's IP
            container_access = ContainerAccess(
                host_ip=get_host_ip(),
                names=container.aliases,
                ports=None,
                forwards=dict((port, published_port) for port, published_port in container.details.published_ports.items()),
            )
        else:
            container_access = None  # no container access without an IP address

        if get_docker_container_id():
            if not container_access:
                raise Exception('Missing IP address for container: %s' % name)

            origin_context = origin.setdefault(container.context, {})
            origin_context[name] = container_access
        elif not published_access:
            pass  # origin does not have network access to the containers
        else:
            origin_context = origin.setdefault(container.context, {})
            origin_context[name] = published_access

        if args.remote:
            pass  # SSH forwarding required
        elif args.docker or get_docker_container_id():
            if container_access:
                control_context = control.setdefault(container.context, {})
                control_context[name] = container_access
            else:
                raise Exception('Missing IP address for container: %s' % name)
        else:
            if not published_access:
                raise Exception('Missing published ports for container: %s' % name)

            control_context = control.setdefault(container.context, {})
            control_context[name] = published_access

    data = {
        HostType.origin: origin,
        HostType.control: control,
        HostType.managed: managed,
    }

    data = dict((key, value) for key, value in data.items() if value)

    return ContainerDatabase(data)


class SupportContainerContext:
    """Context object for tracking information relating to access of support containers."""
    def __init__(self, containers, process):  # type: (ContainerDatabase, t.Optional[SshProcess]) -> None
        self.containers = containers
        self.process = process

    def close(self):  # type: () -> None
        """Close the process maintaining the port forwards."""
        if not self.process:
            return  # forwarding not in use

        self.process.terminate()

        display.info('Waiting for the session SSH port forwarding process to terminate.', verbosity=1)

        self.process.wait()


@contextlib.contextmanager
def support_container_context(
        args,  # type: EnvironmentConfig
        ssh,  # type: t.Optional[SshConnectionDetail]
):  # type: (...) -> t.Optional[ContainerDatabase]
    """Create a context manager for integration tests that use support containers."""
    if not isinstance(args, IntegrationConfig):
        yield None  # containers are only used for integration tests
        return

    containers = get_container_database(args)

    if not containers.data:
        yield ContainerDatabase({})  # no containers are being used, return an empty database
        return

    context = create_support_container_context(args, ssh, containers)

    try:
        yield context.containers
    finally:
        context.close()


def create_support_container_context(
        args,  # type: EnvironmentConfig
        ssh,  # type: t.Optional[SshConnectionDetail]
        containers,  # type: ContainerDatabase
):  # type: (...) -> SupportContainerContext
    """Context manager that provides SSH port forwards. Returns updated container metadata."""
    host_type = HostType.control

    revised = ContainerDatabase(containers.data.copy())
    source = revised.data.pop(HostType.origin, None)

    container_map = {}  # type: t.Dict[t.Tuple[str, int], t.Tuple[str, str, int]]

    if host_type not in revised.data:
        if not source:
            raise Exception('Missing origin container details.')

        for context_name, context in source.items():
            for container_name, container in context.items():
                for port, access_port in container.port_map():
                    container_map[(container.host_ip, access_port)] = (context_name, container_name, port)

    if not container_map:
        return SupportContainerContext(revised, None)

    if not ssh:
        raise Exception('The %s host was not pre-configured for container access and SSH forwarding is not available.' % host_type)

    forwards = list(container_map.keys())
    process = create_ssh_port_forwards(args, ssh, forwards)
    result = SupportContainerContext(revised, process)

    try:
        port_forwards = process.collect_port_forwards()
        contexts = {}

        for forward, forwarded_port in port_forwards.items():
            access_host, access_port = forward
            context_name, container_name, container_port = container_map[(access_host, access_port)]
            container = source[context_name][container_name]
            context = contexts.setdefault(context_name, {})

            forwarded_container = context.setdefault(container_name, ContainerAccess('127.0.0.1', container.names, None, {}))
            forwarded_container.forwards[container_port] = forwarded_port

            display.info('Container "%s" port %d available at %s:%d is forwarded over SSH as port %d.' % (
                container_name, container_port, access_host, access_port, forwarded_port,
            ), verbosity=1)

        revised.data[host_type] = contexts

        return result
    except Exception:
        result.close()
        raise


class ContainerDescriptor:
    """Information about a support container."""
    def __init__(self,
                 image,  # type: str
                 context,  # type: str
                 name,  # type: str
                 container_id,  # type: str
                 ports,  # type: t.List[int]
                 aliases,  # type: t.List[str]
                 publish_ports,  # type: bool
                 running,  # type: bool
                 existing,  # type: bool
                 cleanup,  # type: bool
                 env,  # type: t.Optional[t.Dict[str, str]]
                 ):  # type: (...) -> None
        self.image = image
        self.context = context
        self.name = name
        self.container_id = container_id
        self.ports = ports
        self.aliases = aliases
        self.publish_ports = publish_ports
        self.running = running
        self.existing = existing
        self.cleanup = cleanup
        self.env = env
        self.details = None  # type: t.Optional[SupportContainer]

    def start(self, args):  # type: (EnvironmentConfig) -> None
        """Start the container. Used for containers which are created, but not started."""
        docker_start(args, self.name)

    def register(self, args):  # type: (EnvironmentConfig) -> SupportContainer
        """Record the container's runtime details. Must be used after the container has been started."""
        if self.details:
            raise Exception('Container already registered: %s' % self.name)

        try:
            container = docker_inspect(args, self.container_id)
        except ContainerNotFoundError:
            if not args.explain:
                raise

            # provide enough mock data to keep --explain working
            container = DockerInspect(args, dict(
                Id=self.container_id,
                NetworkSettings=dict(
                    IPAddress='127.0.0.1',
                    Ports=dict(('%d/tcp' % port, [dict(HostPort=random.randint(30000, 40000) if self.publish_ports else port)]) for port in self.ports),
                ),
                Config=dict(
                    Env=['%s=%s' % (key, value) for key, value in self.env.items()] if self.env else [],
                ),
            ))

        support_container_ip = container.get_ip_address()

        if self.publish_ports:
            # inspect the support container to locate the published ports
            tcp_ports = dict((port, container.get_tcp_port(port)) for port in self.ports)

            if any(not config or len(config) != 1 for config in tcp_ports.values()):
                raise ApplicationError('Unexpected `docker inspect` results for published TCP ports:\n%s' % json.dumps(tcp_ports, indent=4, sort_keys=True))

            published_ports = dict((port, int(config[0]['HostPort'])) for port, config in tcp_ports.items())
        else:
            published_ports = {}

        self.details = SupportContainer(
            container,
            support_container_ip,
            published_ports,
        )

        return self.details


class SupportContainer:
    """Information about a running support container available for use by tests."""
    def __init__(self,
                 container,  # type: DockerInspect
                 container_ip,  # type: str
                 published_ports,  # type: t.Dict[int, int]
                 ):  # type: (...) -> None
        self.container = container
        self.container_ip = container_ip
        self.published_ports = published_ports


def wait_for_file(args,  # type: EnvironmentConfig
                  container_name,  # type: str
                  path,  # type: str
                  sleep,  # type: int
                  tries,  # type: int
                  check=None,  # type: t.Optional[t.Callable[[str], bool]]
                  ):  # type: (...) -> str
    """Wait for the specified file to become available in the requested container and return its contents."""
    display.info('Waiting for container "%s" to provide file: %s' % (container_name, path))

    for _iteration in range(1, tries):
        if _iteration > 1:
            time.sleep(sleep)

        try:
            stdout = docker_exec(args, container_name, ['dd', 'if=%s' % path], capture=True)[0]
        except SubprocessError:
            continue

        if not check or check(stdout):
            return stdout

    raise ApplicationError('Timeout waiting for container "%s" to provide file: %s' % (container_name, path))


def cleanup_containers(args):  # type: (EnvironmentConfig) -> None
    """Clean up containers."""
    for container in support_containers.values():
        if container.cleanup:
            docker_rm(args, container.container_id)
        else:
            display.notice('Remember to run `docker rm -f %s` when finished testing.' % container.name)


def create_hosts_entries(context):  # type: (t.Dict[str, ContainerAccess]) -> t.List[str]
    """Return hosts entries for the specified context."""
    entries = []
    unique_id = uuid.uuid4()

    for container in context.values():
        # forwards require port redirection through localhost
        if container.forwards:
            host_ip = '127.0.0.1'
        else:
            host_ip = container.host_ip

        entries.append('%s %s # ansible-test %s' % (host_ip, ' '.join(container.names), unique_id))

    return entries


def create_container_hooks(
        args,  # type: IntegrationConfig
        managed_connections,  # type: t.Optional[t.List[SshConnectionDetail]]
):  # type: (...) -> t.Tuple[t.Optional[t.Callable[[IntegrationTarget], None]], t.Optional[t.Callable[[IntegrationTarget], None]]]
    """Return pre and post target callbacks for enabling and disabling container access for each test target."""
    containers = get_container_database(args)

    control_contexts = containers.data.get(HostType.control)

    if control_contexts:
        managed_contexts = containers.data.get(HostType.managed)

        if not managed_contexts:
            managed_contexts = create_managed_contexts(control_contexts)

        control_type = 'posix'

        if isinstance(args, WindowsIntegrationConfig):
            managed_type = 'windows'
        else:
            managed_type = 'posix'

        control_state = {}
        managed_state = {}

        control_connections = [local_ssh(args)]

        def pre_target(target):
            forward_ssh_ports(args, control_connections, '%s_hosts_prepare.yml' % control_type, control_state, target, HostType.control, control_contexts)
            forward_ssh_ports(args, managed_connections, '%s_hosts_prepare.yml' % managed_type, managed_state, target, HostType.managed, managed_contexts)

        def post_target(target):
            cleanup_ssh_ports(args, control_connections, '%s_hosts_restore.yml' % control_type, control_state, target, HostType.control)
            cleanup_ssh_ports(args, managed_connections, '%s_hosts_restore.yml' % managed_type, managed_state, target, HostType.managed)
    else:
        pre_target, post_target = None, None

    return pre_target, post_target


def create_managed_contexts(control_contexts):  # type: (t.Dict[str, t.Dict[str, ContainerAccess]]) -> t.Dict[str, t.Dict[str, ContainerAccess]]
    """Create managed contexts from the given control contexts."""
    managed_contexts = {}

    for context_name, control_context in control_contexts.items():
        managed_context = managed_contexts[context_name] = {}

        for container_name, control_container in control_context.items():
            managed_context[container_name] = ContainerAccess(control_container.host_ip, control_container.names, None, dict(control_container.port_map()))

    return managed_contexts


def forward_ssh_ports(
        args,  # type: IntegrationConfig
        ssh_connections,  # type: t.Optional[t.List[SshConnectionDetail]]
        playbook,  # type: str
        target_state,  # type: t.Dict[str, t.Tuple[t.List[str], t.List[SshProcess]]]
        target,  # type: IntegrationTarget
        host_type,  # type: str
        contexts,  # type: t.Dict[str, t.Dict[str, ContainerAccess]]
):  # type: (...) -> None
    """Configure port forwarding using SSH and write hosts file entries."""
    if ssh_connections is None:
        return

    test_context = None

    for context_name, context in contexts.items():
        context_alias = 'cloud/%s/' % context_name

        if context_alias in target.aliases:
            test_context = context
            break

    if not test_context:
        return

    if not ssh_connections:
        raise Exception('The %s host was not pre-configured for container access and SSH forwarding is not available.' % host_type)

    redirects = []  # type: t.List[t.Tuple[int, str, int]]
    messages = []

    for container_name, container in test_context.items():
        explain = []

        for container_port, access_port in container.port_map():
            if container.forwards:
                redirects.append((container_port, container.host_ip, access_port))

                explain.append('%d -> %s:%d' % (container_port, container.host_ip, access_port))
            else:
                explain.append('%s:%d' % (container.host_ip, container_port))

        if explain:
            if container.forwards:
                message = 'Port forwards for the "%s" container have been established on the %s host' % (container_name, host_type)
            else:
                message = 'Ports for the "%s" container are available on the %s host as' % (container_name, host_type)

            messages.append('%s:\n%s' % (message, '\n'.join(explain)))

    hosts_entries = create_hosts_entries(test_context)
    inventory = generate_ssh_inventory(ssh_connections)

    with named_temporary_file(args, 'ssh-inventory-', '.json', None, inventory) as inventory_path:
        run_playbook(args, inventory_path, playbook, dict(hosts_entries=hosts_entries))

    ssh_processes = []  # type: t.List[SshProcess]

    if redirects:
        for ssh in ssh_connections:
            ssh_processes.append(create_ssh_port_redirects(args, ssh, redirects))

    target_state[target.name] = (hosts_entries, ssh_processes)

    for message in messages:
        display.info(message, verbosity=1)


def cleanup_ssh_ports(
        args,  # type: IntegrationConfig
        ssh_connections,  # type: t.List[SshConnectionDetail]
        playbook,  # type: str
        target_state,  # type: t.Dict[str, t.Tuple[t.List[str], t.List[SshProcess]]]
        target,  # type: IntegrationTarget
        host_type,  # type: str
):  # type: (...) -> None
    """Stop previously configured SSH port forwarding and remove previously written hosts file entries."""
    state = target_state.pop(target.name, None)

    if not state:
        return

    (hosts_entries, ssh_processes) = state

    inventory = generate_ssh_inventory(ssh_connections)

    with named_temporary_file(args, 'ssh-inventory-', '.json', None, inventory) as inventory_path:
        run_playbook(args, inventory_path, playbook, dict(hosts_entries=hosts_entries))

    if ssh_processes:
        for process in ssh_processes:
            process.terminate()

        display.info('Waiting for the %s host SSH port forwarding processs(es) to terminate.' % host_type, verbosity=1)

        for process in ssh_processes:
            process.wait()
