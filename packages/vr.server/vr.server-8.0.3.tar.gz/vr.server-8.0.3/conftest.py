import os
import sys
import functools

import pytest
from django import setup
import portend
import redis
import jaraco.context

from vr.server.tests import dbsetup


def _path_hack():
    """
    hack the PYTHONPATH to ensure that re-entrant processes
    have access to packages loaded by pytest-runner.
    """
    os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)


def pytest_configure():
    """
    Setup the django instance before to run the tests

    Starting from django 1.7 we need to let django to setup itself.
    """
    _path_hack()
    setup()
    _setup_allowed_hosts()


def _setup_allowed_hosts():
    '''Allow the hostname we use for testing.'''
    from django.conf import settings
    settings.ALLOWED_HOSTS = ['testserver']


@pytest.fixture(scope="session")
def gridfs(mongodb_instance):
    from django.conf import settings
    settings.GRIDFS_PORT = mongodb_instance.port
    settings.MONGODB_URL = mongodb_instance.get_uri() + '/velociraptor'
    patch_default_storage()


def patch_default_storage():
    """
    By the time the tests run, django has already started up
    and configured the default_storage for files, binding the
    GridFSStorage to the default host/port. But the test suite
    has gone to a lot of trouble to supply an ephemeral instance
    of MongoDB, so re-init the default storage to use that
    instance.
    """
    import django
    django.core.files.storage.default_storage.__init__()


@pytest.fixture
def postgresql(request):
    if request.config.getoption('--use-local-db'):
        dbsetup()
        return

    postgresql_instance = request.getfuncargvalue('postgresql_instance')
    from django.conf import settings
    settings.DATABASES['default']['PORT'] = str(postgresql_instance.port)
    dbsetup(postgresql_instance.port)
    return postgresql_instance


def check_redis(port):
    return redis.StrictRedis(host='localhost', port=port).echo('this')


def redis_running(port):
    with jaraco.context.ExceptionTrap() as trap:
        check_redis(port)
    return not bool(trap)


@pytest.fixture(scope='session')
def redis_instance(watcher_getter, request):
    port = portend.find_available_local_port()
    proc = watcher_getter( # noqa
        name='redis-server',
        arguments=[
            '--port', str(port),
        ],
        checker=functools.partial(redis_running, port=port),
        request=request,
    )
    client = redis.StrictRedis(host='localhost', port=port)
    return locals()


@pytest.fixture(name='redis', scope='session')
def redis_(request):
    try:
        instance = request.getfixturevalue('redis_instance')
    except Exception:
        instance = request.getfixturevalue('redis_local')
    url = 'redis://localhost:{port}/0'.format(**instance)
    netloc = 'localhost:{port}'.format(**instance)
    from django.conf import settings
    settings.EVENTS_PUBSUB_URL = url
    settings.CACHES['default']['LOCATION'] = netloc
    settings.CELERYBEAT_SCHEDULE_FILENAME = url
    settings.BROKER_URL = url
    settings.CELERY_RESULT_BACKEND = url
    return instance


@pytest.fixture(scope='session')
def redis_local():
    client = redis.StrictRedis('localhost')
    client.echo('this')
    return dict(locals(), port=6379)


def pytest_addoption(parser):
    parser.addoption(
        '--use-local-db', action='store_true',
        default=False,
        help="Use a local, already configured database",
    )
