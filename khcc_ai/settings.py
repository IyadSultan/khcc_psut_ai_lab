INSTALLED_APPS = [
    ...
    'gold_analytics.apps.GoldAnalyticsConfig',
]

MIDDLEWARE = [
    ...
    'gold_analytics.middleware.AnalyticsMiddleware',
] 