# -*- coding: utf-8 -*-
"""
Main module - tripod main module.
"""
import inspect
import os
import sys
from invoke import Collection, Program, Task
from . import utils
from .config import Config
from .local import LocalProxy
from .exceptions import BadConfigurationError
import pathlib


class Main(Program):
    """The tripod main class. Holds the main function.
    """
    def __init__(
            self, version=None,
        namespace=None,
        name=None,
        binary=None,
        loader_class=None,
        executor_class=None,
        config_class=None
    ):
        """
        Create a new, parameterized `.Program` instance.

        :param str version:
            The program's version, e.g. ``"0.1.0"``. Defaults to ``"unknown"``.

        :param namespace:
            A `.Collection` to use as this program's subcommands.

            If ``None`` (the default), the program will behave like ``invoke``,
            seeking a nearby task namespace with a `.Loader` and exposing
            arguments such as :option:`--list` and :option:`--collection` for
            inspecting or selecting specific namespaces.

            If given a `.Collection` object, will use it as if it had been
            handed to :option:`--collection`. Will also update the parser to
            remove references to tasks and task-related options, and display
            the subcommands in ``--help`` output. The result will be a program
            that has a static set of subcommands.

        :param str name:
            The program's name, as displayed in ``--version`` output.

            If ``None`` (default), is a capitalized version of the first word
            in the ``argv`` handed to `.run`. For example, when invoked from a
            binstub installed as ``foobar``, it will default to ``Foobar``.

        :param str binary:
            The binary name as displayed in ``--help`` output.

            If ``None`` (default), uses the first word in ``argv`` verbatim (as
            with ``name`` above, except not capitalized).

            Giving this explicitly may be useful when you install your program
            under multiple names, such as Invoke itself does - it installs as
            both ``inv`` and ``invoke``, and sets ``binary="inv[oke]"`` so its
            ``--help`` output implies both names.

        :param loader_class:
            The `.Loader` subclass to use when loading task collections.

            Defaults to `.FilesystemLoader`.

        :param executor_class:
            The `.Executor` subclass to use when executing tasks.

            Defaults to `.Executor`.

        :param config_class:
            The `.Config` subclass to use for the base config object.

            Defaults to `.Config`.
        """
        super().__init__(
            version=version,
            namespace=namespace,
            name=name,
            binary=binary,
            loader_class=loader_class,
            executor_class=executor_class,
            config_class=config_class
        )
        # tripod config setup
        self.app_config = Main.get_config()
        # tripod tasks namespace is a simple invoke.Collection object
        if namespace is None:
            self.namespace = Collection()
        # tripod needs to discover its self task functions
        current_dir = os.path.dirname(__file__)
        # run tripod discovery function to find its own command line functions
        from tripod import tasks
        self.namespace.add_task(tasks.run)
        self.namespace.add_task(tasks.test)

        # get tripod project home path from the tripod configuration or
        # set the current working directory in the sys.path as the project home
        # tripod_home path enables tripod capabilities such as blueprints auto discover
        # and automatic script finding
        self.project_root = self.app_config.get("TRIPOD.HOME_DIR", os.getcwd())  # tripod terminal root
        # expands current user path
        if self.project_root.startswith('~'):
            self.project_root = os.path.join(os.path.expanduser('~'), self.project_root[2:])
        # insert project root to the sys path
        sys.path.insert(0, self.project_root)
        # set the environment current directory to the project root path
        os.chdir(self.project_root)

        # discover project custom tasks
        self.discover_tasks(self.project_root)
        # initialize app with None
        self.app = None

    def discover_tasks(self, path):
        """A invoke task discovery function.

        :param path: a root path to be used during the task discovery.
        """
        def task_selector(member):
            """Filters modules members that are instances of 'invoke.Task' class."""
            if isinstance(member, (Task,)):
                return True
            return False

        _no_selection = lambda finder, name, is_pack: True

        # custom tasks registration
        if os.path.exists(os.path.join(path, "tasks")):
            # if there is a tasks directory then run autodiscover function on that directory
            # and register all task that are found on the tripod namespace
            for mod, members in utils.auto_discover(_no_selection, task_selector, os.path.join(path, "tasks")):
                # if module has tasks objects
                if len(members) > 0:
                    # then register tasks on the tripod namespace
                    # if module file name is tasks.py
                    if str(mod.__file__).endswith("tasks.py"):
                        # then register tasks on the root tripod namespace
                        for name, t in members:
                            self.namespace.add_task(t, t.name)
                    else:  # otherwise register tasks using dotted namespace.
                        # using the following syntax `tripod mod_name.task-name`
                        self.namespace.add_collection(mod)

        elif os.path.exists(os.path.join(path, "tasks.py")):
            # if we could not find the tasks directory then we look for a tasks.py file on the project root directory
            # and then we register all tasks found on that file on the tripod tasks namespace.
            name = inspect.getmodulename(os.path.join(path, "tasks.py"))
            mod = utils.import_module(name)
            for name, t in inspect.getmembers(mod, predicate=task_selector):
                self.namespace.add_task(t, t.name)

    @staticmethod
    def get_config():
        """ A configuration loader function.
        Builds the configuration object, loads the configuration from the specified files
        and then returns it.
        :return: a Config object.
        """
        config = Config()
        home_dir = pathlib.Path.home()
        config.add_path(str(home_dir/".config/tripod/tripod.cfg"))
        config.add_path(str(home_dir/".config/tripod/tripod.yaml"))
        config.add_path(str(home_dir/".config/tripod/tripod.json"))
        # load tripod configuration
        config.load_config()
        home_dir = config.get("TRIPOD.HOME_DIR", os.getcwd())
        environment = config.get("TRIPOD.ENVIRONMENT")
        if environment is not None:
            config.add_path(os.path.join(home_dir, "settings/{}/settings.py".format(environment)))

        config.add_path(os.path.join(home_dir, "settings/settings.py"))
        config.add_path(os.path.join(home_dir, "settings.py"))
        config.load_config()
        return config

    def init_app(self, dev=False, single=False):
        """
        Builds the application based on its "type" (i.e. supervisord app or flask)
        and sets it to the current_app context.
        :param dev: true if it should be built on development mode
        :param single: if app type is supervisord,
        this flag indicates whether it should build a supervisord instance or a app instance.
        """
        app_type = self.app_config.get("TRIPOD.APP_TYPE", None)

        if app_type == "DAEMON":
            from .builders.daemon_builder import build_app
            self.app = build_app(dev, single, self)

            from .application.supervisor import SupervisordApp
            if not isinstance(self.app, SupervisordApp):
                self.app.events.after_app_init.send(self.app)

        elif app_type == "FLASK":
            from .builders.flask_loaders import build_app
            self.app = build_app(dev, self)
            from .application.flask import FlaskApp
            if isinstance(self.app, FlaskApp):
                self.app.events.after_app_init.send(self.app)
        else:
            raise BadConfigurationError(
                "Bad 'app_type' configuration was found. "
                "Could not initialize the tripod.App correctly. "
                "Please check the 'TRIPOD.APP_TYPE' configuration to fix this error. "
                "Current value: 'TRIPOD.APP_TYPE'= {}".format(app_type)
            )

    def execute(self):
        """
        Hand off data & tasks-to-execute specification to an `.Executor`.

        .. note::
            Client code just wanting a different `.Executor` subclass can just
            set ``executor_class`` in `.__init__`.
        """
        executor = self.executor_class(self.collection, self.config, self.core)

        # get app initialization flags from command line
        dev_flag = self.core_via_tasks.args.dev.value
        single_flag = self.core_via_tasks.args.single.value
        init_app_flag = not self.core_via_tasks.args['init-app'].value

        if init_app_flag:
            self.init_app(dev_flag, single_flag)

        executor.execute(*self.tasks)

    def core_args(self):
        """
        Extends the invoke core argument list with the app initialization flags.
        """
        # Arguments present always, even when wrapped as a different binary
        from invoke import Argument
        core_args = super(Main, self).core_args()
        extra_args = [
            Argument(
                names=('dev',),
                help="Development mode flag.",
                kind=bool,
                default=False,
                optional=True,
            ),
            Argument(
                names=('single',),
                help="Single app instance flag.",
                kind=bool,
                default=False,
                optional=True,
            ),
            Argument(
                names=('init-app', 'i'),
                help="Single app instance flag.",
                kind=bool,
                default=False,
                optional=True
            ),
        ]
        return core_args + extra_args


main = Main()

app = LocalProxy(lambda: main.app)
