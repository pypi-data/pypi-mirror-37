SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'datapunt_api',
    'rest_framework',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.base_urls'

STATIC_ROOT = 'static/'
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

REST_FRAMEWORK = dict(
    PAGE_SIZE=100,

    MAX_PAGINATE_BY=100,
    DEFAULT_PAGINATION_CLASS='datapunt_api.pagination.HALPagination',

    DEFAULT_RENDERER_CLASSES=(
       'rest_framework.renderers.JSONRenderer',
       'datapunt_api.renderers.PaginatedCSVRenderer',
       'rest_framework.renderers.BrowsableAPIRenderer',
       'rest_framework_xml.renderers.XMLRenderer'
    ),

    DEFAULT_FILTER_BACKENDS=(
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    COERCE_DECIMAL_TO_STRING=False,  # other Datapunt projects set this to True
    UNAUTHENTICATED_USER=None,
)
