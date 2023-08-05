"""Plugins support."""

from muffin.utils import LStruct, MuffinException


class PluginException(MuffinException):

    """Implement any exception in plugins."""


class PluginMeta(type):

    """Ensure that each plugin is singleton."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Check for the plugin is initialized already."""
        if not cls.name:
            raise PluginException('Plugin `%s` doesn\'t have a name.' % cls)

        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BasePlugin(metaclass=PluginMeta):

    """Base class for Muffin plugins."""

    # Plugin options with default values
    defaults = {}

    # Plugin dependencies (name: Plugin)
    dependencies = {}

    name = None

    def __init__(self, app=None, **options):
        """Save application and create he plugin's configuration."""
        self.config = self.cfg = LStruct(options)
        self.app = app
        if app is not None:
            app.install(self)

    def setup(self, app):
        """Initialize the plugin.

        Fill the plugin's options from application.
        """
        self.app = app
        for name, ptype in self.dependencies.items():
            if name not in app.ps or not isinstance(app.ps[name], ptype):
                raise PluginException(
                    'Plugin `%s` requires for plugin `%s` to be installed to the application.' % (
                        self.name, ptype))

        for oname, dvalue in self.defaults.items():
            aname = ('%s_%s' % (self.name, oname)).upper()
            self.cfg.setdefault(oname, app.cfg.get(aname, dvalue))
            app.cfg.setdefault(aname, self.cfg[oname])
