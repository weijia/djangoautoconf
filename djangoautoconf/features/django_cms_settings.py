INSTALLED_APPS += (
    'django.contrib.sites',
    'cms',
    'menus',
    'treebeard',
)

MIDDLEWARE_CLASSES += (
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)


TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]
