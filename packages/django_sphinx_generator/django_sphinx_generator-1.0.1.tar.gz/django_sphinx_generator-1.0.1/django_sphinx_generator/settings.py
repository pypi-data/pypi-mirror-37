
from django.conf import settings

DEFAULT_SETTINGS = {
    'path': 'doc/source/code',
    'namespace': 'apps',
    'components': [
        {
            'title': 'Models',
            'path': 'models',
        },
        {
            'title': 'Serializers',
            'path': 'serializers',
        },
        {
            'title': 'Signals',
            'path': 'signals',
        },
        {
            'title': 'Filters',
            'path': 'filters',
        },
        {
            'title': 'Views',
            'path': 'views',
        },
        {
            'title': 'Management',
            'path': 'management',
        },
        {
            'title': 'Tasks',
            'path': 'tasks',
        },
        {
            'title': 'Unit tests',
            'path': 'test',
        },
        {
            'title': 'Schemas',
            'path': 'schemas',
        },
        {
            'title': 'URL configuration',
            'path': 'urls',
        },
    ]
}


SPHINX_DOCUMENT_GENERATOR = getattr(settings, 'SPHINX_DOCUMENT_GENERATOR', DEFAULT_SETTINGS)
