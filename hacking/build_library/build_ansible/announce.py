# coding: utf-8
# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import asyncio
import datetime
import hashlib

import aiohttp
from jinja2 import Environment, DictLoader


VERSION_FRAGMENT = """
{%- if versions | length > 1 %}
  {% for version in versions %}
    {% if loop.last %}and {{ version }}{% else %}
      {% if versions | length == 2 %}{{ version }} {% else %}{{ version }}, {% endif -%}
    {% endif -%}
  {% endfor -%}
{%- else %}{{ versions[0] }}{% endif -%}
"""

LONG_TEMPLATE = """
{% set plural = False if versions | length == 1 else True %}
{% set latest_ver = (versions | sort(attribute='ver_obj'))[-1] %}

To: ansible-devel@googlegroups.com, ansible-project@googlegroups.com, ansible-announce@googlegroups.com
Subject: New Ansible release{% if plural %}s{% endif %} {{ version_str }}

{% filter wordwrap %}
Hi all- we're happy to announce that the general release of Ansible {{ version_str }}{% if plural %} are{%- else %} is{%- endif %} now available!
{% endfilter %}



How do you get it?
------------------

{% for version in versions %}
$ pip install ansible=={{ version }} --user
{% if not loop.last %}
or
{% endif %}
{% endfor %}

The tar.gz of the release{% if plural %}s{% endif %} can be found here:

{% for version in versions %}
* {{ version }}
  https://releases.ansible.com/ansible/ansible-{{ version }}.tar.gz
  SHA256: {{ hashes[version] }}
{% endfor %}


What's new in {{ version_str }}
{{ '-' * (14 + version_str | length) }}

{% filter wordwrap %}
{% if plural %}These releases are{% else %}This release is a{% endif %} maintenance release{% if plural %}s{% endif %} containing numerous bugfixes. The full {% if plural %} changelogs are{% else %} changelog is{% endif %} at:
{% endfilter %}


{% for version in versions %}
* {{ version }}
  https://github.com/ansible/ansible/blob/stable-{{ version.split('.')[:2] | join('.') }}/changelogs/CHANGELOG-v{{ version.split('.')[:2] | join('.') }}.rst
{% endfor %}


What's the schedule for future maintenance releases?
----------------------------------------------------

{% filter wordwrap %}
Future maintenance releases will occur approximately every 3 weeks.  So expect the next one around {{ next_release.strftime('%Y-%m-%d') }}.
{% endfilter %}



Porting Help
------------

{% filter wordwrap %}
We've published a porting guide at
https://docs.ansible.com/ansible/devel/porting_guides/porting_guide_{{ latest_ver.split('.')[:2] | join('.') }}.html to help migrate your content to {{ latest_ver.split('.')[:2] | join('.') }}.
{% endfilter %}



{% filter wordwrap %}
If you discover any errors or if any of your working playbooks break when you upgrade to {{ latest_ver }}, please use the following link to report the regression:
{% endfilter %}


  https://github.com/ansible/ansible/issues/new/choose

{% filter wordwrap %}
In your issue, be sure to mention the Ansible version that works and the one that doesn't.
{% endfilter %}


Thanks!

-{{ name }}

"""  # noqa for E501 (line length).
# jinja2 is horrid about getting rid of extra newlines so we have to have a single per paragraph for
# proper wrapping to occur

SHORT_TEMPLATE = """
{% set plural = False if versions | length == 1 else True %}
@ansible
{{ version_str }}
{% if plural %}
  have
{% else %}
  has
{% endif %}
been released! Get
{% if plural %}
them
{% else %}
it
{% endif %}
on PyPI: pip install ansible=={{ (versions|sort(attribute='ver_obj'))[-1] }},
https://releases.ansible.com/ansible/, the Ansible PPA on Launchpad, or GitHub.  Happy automating!
"""  # noqa for E501 (line length).
# jinja2 is horrid about getting rid of extra newlines so we have to have a single per paragraph for
# proper wrapping to occur

JINJA_ENV = Environment(
    loader=DictLoader({'long': LONG_TEMPLATE,
                       'short': SHORT_TEMPLATE,
                       'version_string': VERSION_FRAGMENT,
                       }),
    extensions=['jinja2.ext.i18n'],
    trim_blocks=True,
    lstrip_blocks=True,
)


async def calculate_hash_from_tarball(session, version):
    tar_url = f'https://releases.ansible.com/ansible/ansible-{version}.tar.gz'
    tar_task = asyncio.create_task(session.get(tar_url))
    tar_response = await tar_task

    tar_hash = hashlib.sha256()
    while True:
        chunk = await tar_response.content.read(1024)
        if not chunk:
            break
        tar_hash.update(chunk)

    return tar_hash.hexdigest()


async def parse_hash_from_file(session, version):
    filename = f'ansible-{version}.tar.gz'
    hash_url = f'https://releases.ansible.com/ansible/{filename}.sha'
    hash_task = asyncio.create_task(session.get(hash_url))
    hash_response = await hash_task

    hash_content = await hash_response.read()
    precreated_hash, precreated_filename = hash_content.split(None, 1)
    if filename != precreated_filename.strip().decode('utf-8'):
        raise ValueError(f'Hash file contains hash for a different file: {precreated_filename}')

    return precreated_hash.decode('utf-8')


async def get_hash(session, version):
    calculated_hash = await calculate_hash_from_tarball(session, version)
    precreated_hash = await parse_hash_from_file(session, version)

    if calculated_hash != precreated_hash:
        raise ValueError(f'Hash in file ansible-{version}.tar.gz.sha {precreated_hash} does not'
                         f' match hash of tarball {calculated_hash}')

    return calculated_hash


async def get_hashes(versions):
    hashes = {}
    requestors = {}
    async with aiohttp.ClientSession() as aio_session:
        for version in versions:
            requestors[version] = asyncio.create_task(get_hash(aio_session, version))

        for version, request in requestors.items():
            await request
            hashes[version] = request.result()

    return hashes


def next_release_date(weeks=3):
    days_in_the_future = weeks * 7
    today = datetime.datetime.now()
    numeric_today = today.weekday()

    # We release on Thursdays
    if numeric_today == 3:
        # 3 is Thursday
        pass
    elif numeric_today == 4:
        # If this is Friday, we can adjust back to Thursday for the next release
        today -= datetime.timedelta(days=1)
    elif numeric_today < 3:
        # Otherwise, slide forward to Thursday
        today += datetime.timedelta(days=(3 - numeric_today))
    else:
        # slightly different formula if it's past Thursday this week.  We need to go forward to
        # Thursday of next week
        today += datetime.timedelta(days=(10 - numeric_today))

    next_release = today + datetime.timedelta(days=days_in_the_future)
    return next_release


def create_long_message(versions, name):
    hashes = asyncio.run(get_hashes(versions))

    version_template = JINJA_ENV.get_template('version_string')
    version_str = version_template.render(versions=versions).strip()

    next_release = next_release_date()

    template = JINJA_ENV.get_template('long')
    message = template.render(versions=versions, version_str=version_str,
                              name=name, hashes=hashes, next_release=next_release)
    return message


def create_short_message(versions):
    version_template = JINJA_ENV.get_template('version_string')
    version_str = version_template.render(versions=versions).strip()

    template = JINJA_ENV.get_template('short')
    message = template.render(versions=versions, version_str=version_str)
    message = ' '.join(message.split()) + '\n'
    return message
