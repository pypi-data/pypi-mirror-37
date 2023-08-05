
import fnmatch
import os

from django.apps import apps
from django_sphinx_generator.settings import SPHINX_DOCUMENT_GENERATOR as settings
from django.template.loader import render_to_string

# Filename patterns to ignore
IGNORE_PATTERNS = (
    '__pycache__',
    '*.pyc',
)
# Filenames to exclude from document tree
IGNORE_NAMES = (
    '__init__.py',
)


class DocumentGeneratorError(Exception):
    """
    Exceptions caused by document generator
    """
    pass


class SphinxDocumentIndex:
    """
    Common parent class for sphinx document tree items
    """

    @property
    def index(self):
        return '{}/index.rst'.format(self.path)

    def create_directory(self):
        """
        Create directory to sphinx documentation tree
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        return self.path


class Module(SphinxDocumentIndex):
    """
    App component for documentation
    """
    caption = 'Module Contents'

    def __init__(self, app, name, title):
        self.app = app
        self.name = name
        self.title = title
        self.path = os.sep.join([self.app.path, self.name])
        self.modules = []
        self.files = []

    def __repr__(self):
        return self.name

    def add_module(self, filename):
        """
        Add source code module to component
        """
        name = '{}.{}'.format(
            self.app.module_name,
            filename[
                len(self.app.app.path) + 1:
            ].lstrip(os.sep).replace('.py', '').replace(os.sep, '.')
        )

        if name in self.app.generator.module_paths:
            return

        # Test importing module before adding
        try:
            __import__(name)
            self.modules.append(name)
        except ImportError as e:
            DocumentGeneratorError('Error importing component {} ({}): {}'.format(
                name,
                filename,
                e
            ))

    def add_file(self, filename):
        """
        Add source code file to component
        """
        def has_callables(name, filename):
            """
            Check if there are any local functions or classes in module

            No point adding a file that has nothing to document.
            """
            try:
                parent = '.'.join(name.split('.')[:-1])
                attr = name.split('.')[-1]
                obj = getattr(__import__(parent, fromlist=[attr]), attr)
                for field in obj.__dir__():
                    obj_attr = getattr(obj, field)
                    # Check if field is callable
                    if not callable(obj_attr):
                        continue
                    # Check if field is from this module
                    if getattr(obj_attr, '__module__', None) != name:
                        continue
                    # Looks OK, return True
                    return True
                return False
            except ImportError as e:
                DocumentGeneratorError('Error importing component {} ({}): {}'.format(
                    name,
                    filename,
                    e
                ))

        name = '{}.{}'.format(
            self.app.module_name,
            filename[
                len(self.app.app.path) + 1:
            ].lstrip(os.sep).replace('.py', '').replace(os.sep, '.')
        )

        if name in self.app.generator.module_paths:
            return

        if has_callables(name, filename):
            self.files.append(name)

    def create_indexes(self):
        """
        Create index.rst file with specified components using template
        """

        with open(self.index, 'w') as fd:
            fd.write(render_to_string(
                'django_sphinx_generator/modules.rst.j2',
                {
                    'title': self.title,
                    'caption': self.caption,
                    'modules': self.modules,
                    'files': self.files,
                }
            ))


class App(SphinxDocumentIndex):
    """
    Django app for document generation
    """
    caption = 'Modules'

    def __init__(self, generator, app):
        self.generator = generator
        self.app = app
        self.path = os.sep.join([self.generator.path, self.label])
        self.modules = []
        self.files = []
        self.detect_modules()

    def __repr__(self):
        return self.label

    @property
    def label(self):
        return self.app.label

    @property
    def title(self):
        return self.app.verbose_name

    @property
    def description(self):
        """
        Long description for module
        """
        try:
            return getattr(__import__(
                self.module_name, globals(), fromlist=['apps']
            ), 'apps').APP_DESCRIPTION_DOCSTRING
        except ImportError:
            return None
        except AttributeError:
            return None

    @property
    def module_name(self):
        return self.app.module.__name__

    def detect_modules(self):
        """
        Detect code modules in app
        """

        def is_ignored_filename(path):
            for pattern in IGNORE_PATTERNS:
                if fnmatch.fnmatch(path, pattern):
                    return True
            return False

        # Detect named components
        for component in self.generator.components_config:
            path = os.sep.join([self.app.path, component['path']])

            module_paths = []
            file_paths = []
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for filename in files:
                        if filename in IGNORE_NAMES:
                            continue
                        if not os.path.splitext(filename)[1] == '.py':
                            continue
                        filename = os.sep.join([root, filename])
                        if is_ignored_filename(filename):
                            continue
                        module_paths.append(filename)

            else:
                filename = '{}.py'.format(path)
                if os.path.isfile(filename):
                    file_paths.append(filename)

            module = Module(
                self,
                component['path'],
                component['title'],
            )

            for filename in module_paths:
                module.add_module(filename)

            for filename in file_paths:
                module.add_file(filename)

            if module.modules:
                self.modules.append(module)

        for filename in os.listdir(self.app.path):
            if filename in IGNORE_NAMES:
                continue
            path = os.sep.join([self.app.path, filename])
            if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
                continue

            # Detect additional python files in app directory
            name = os.path.splitext(filename)[0]
            module = Module(
                self,
                name,
                name,
            )
            module.add_file(path)

            if module.files:
                self.files.append(module)

    def create_index(self):
        """
        Create index.rst file with specified components using template
        """

        with open(self.index, 'w') as fd:
            fd.write(render_to_string(
                'django_sphinx_generator/module_index.rst.j2',
                {
                    'title': self.title,
                    'description': self.description,
                    'caption': self.caption,
                    'modules': self.modules,
                    'files': self.files,
                }
            ))


class DocumentGenerator:
    """
    Sphinx document tree generator

    Detects django app code and generates sphinx automodule document trees.
    """

    def __init__(self):
        self.path = settings['path']
        self.namespace = settings['namespace'].split('.')
        self.components_config = settings['components']
        self.apps = []

        for app in apps.app_configs.values():
            if app.name.split('.')[:len(self.namespace)] != self.namespace:
                continue
            self.apps.append(App(self, app))

    def __repr__(self):
        return self.path

    @property
    def index(self):
        """
        Path to index file for code documentation tree
        """
        return os.sep.join([self.path, 'index.rst'])

    @property
    def module_paths(self):
        """
        Return IDs of all detected modules
        """
        paths = []
        for app in self.apps:
            if app.path not in paths:
                paths.append(app.path)
            for module in app.modules:
                for module in module.modules:
                    if module not in paths:
                        paths.append(module)
        return paths

    def create_index(self):
        """
        Create index.rst file for all code modules
        """

        with open(self.index, 'w') as fd:
            fd.write(render_to_string(
                'django_sphinx_generator/index.rst.j2',
                {
                    'title': 'Django Apps',
                    'caption': 'Apps',
                    'modules': self.apps,
                }
            ))

    def create_document_tree(self):
        for app in self.apps:
            app.create_directory()
            app.create_index()
            for item in app.modules:
                item.create_directory()
                item.create_indexes()

            for item in app.files:
                item.create_directory()
                item.create_indexes()

        self.create_index()
