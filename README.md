# Ansible Collection - inspq.keycloak

Documentation for the collection.

## Testing locally

The integration tests expect a keycloak instance to be reachable trhough `http://keycloak:8080`.
You can start a container locally to serve this url:

```
$ docker run --rm -it --name keycloak -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -d jboss/keycloak
```

## Run integration tests

```
$ ansible-test integration -v --docker
```

You can specify the python version you want to use:

```
$ ansible-test integration -v --docker --python 2.7
```
