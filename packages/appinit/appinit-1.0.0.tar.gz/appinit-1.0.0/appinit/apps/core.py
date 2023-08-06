import os
import re
import subprocess

from .. import utils
from ..environ import Environ


def _iter_entry_points(app_name=None):
    from .. import _vendor
    _vendor.install()
    import pkg_resources
    return pkg_resources.iter_entry_points('appinit_apps', app_name)

def iter_app_classes():
    for ep in _iter_entry_points():
        yield ep.load()


class Version(tuple):

    def __new__(cls, input_):
        if isinstance(input_, basestring):
            str_value = input_
            input_ = map(int, filter(None, re.split(r'\D', input_)))
        elif isinstance(input_, int):
            str_value = str(input_)
            input_ = (input_, )
        else:
            str_value = '.'.join(input_)
        self = super(Version, cls).__new__(cls, input_)
        self._str_value = str_value
        return self

    def __str__(self):
        return self._str_value


class BaseApp(object):

    name = '????'

    @classmethod
    def iter_installed(cls):
        return iter(())

    @classmethod
    def get_running_app(cls):
        pass

    def __init__(self, path=None, version=None):
        self.path = path
        self.version = Version(version)

    def get_envvars(self):
        return {}
    
    def get_python(self):
        return None

    def get_site_packages(self):
        pass
    
    def get_command(self):
        raise NotImplementedError()

    def prepare_command(self, args, command=None, env=None, python=False):

        if python:
            command = [self.get_python()]
        elif command is None:
            command = self.get_command()
        if not command:
            raise ValueError('no command to exec')
        command.extend(args)

        env = Environ(env or os.environ)
        self.export(env)

        return command, env

    def popen(self, *args, **kwargs):
        cmd, env = self.prepare_command(*args, **kwargs)
        return subprocess.Popen(cmd, env=env)

    def exec_(self, *args, **kwargs):
        background = kwargs.pop('background', None)
        cmd, env = self.prepare_command(*args, **kwargs)
        if background:
            utils.daemonize()
        os.execve(cmd[0], cmd, env)



class AppSelector(object):

    def __init__(self, spec):
        if spec is None:
            self.name = self.operation = self.version = None
        else:
            m = re.match(r'^(\w+)(?:(==)([\w.]+))?$', spec)
            if not m:
                raise ValueError('invalid app spec %r' % spec)
            self.name, self.operation, version = m.groups()
            self.version = Version(version) if version else None

    def iter_installed(self):
        for cls_ep in _iter_entry_points(self.name):
            cls = cls_ep.load()
            for app in cls.iter_installed():
                if self.version is None:
                    yield app
                elif self.operation == '==':
                    if self.version == app.version:
                        yield app
                else:
                    # Arguably this should be in the constructor, but this is
                    # more certain to catch errors.
                    raise ValueError('unknown version operation %s' % self.operation)


def _iter_installed_apps(selectors=None):
    selectors = selectors or None
    if not isinstance(selectors, (list, tuple)):
        selectors = [selectors]
    for selector in selectors:
        if isinstance(selector, BaseApp):
            yield selector
            continue
        selector = AppSelector(selector)
        for app in selector.iter_installed():
            yield app

def iter_installed_apps(selectors=None, sort=True):
    iter_ = _iter_installed_apps(selectors)
    if sort:
        return iter(sorted(iter_, key=lambda app: (app.name, [-x for x in app.version])))
    else:
        return iter_

