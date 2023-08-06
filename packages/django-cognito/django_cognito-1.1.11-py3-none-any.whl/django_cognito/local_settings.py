APP_CLIENT_ID = "3kqb3tvmcr6aatg75jpc0dsji0"
APP_SECRET_KEY = "1nih0b258nb1800nkg4iesivh78sv4hhf282or3g2kbuhm2i5mal"
COGNITO_POOL_ID = "ap-southeast-2_WRUdGyjlM"
AWS_ACCESS_KEY = "AKIAJQRQ6OVUWNHCCGMQ"
AWS_SECRET_KEY = "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"
AUTO_CREATE_USER = True
CORS_ALLOW_CREDENTIALS = True


CORS_ORIGIN_WHITELIST = (
    'localhost',
    'api.jana.com.au',
    'app.jana.com.au',
    '127.0.0.1:8095',
    'localhost:4200',
    'dev-api.jana.com.au',
    'dev-app.jana.com.au',
    'uat-app.jana.com.au',
    'uat-app.jana.com.au:9002',
)

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}
