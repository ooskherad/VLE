from pydantic import BaseSettings


class Config(BaseSettings):
    DEBUG = True
    APP_TITLE = "virtual learning environment"

    SECRET_KEY = ''
    DATABASE_NAME = 'vle'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = '1234'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'

    # ARVAN CLOUD STORAGE CONFIG
    DEFAULT_FILE_STORAGE = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_STORAGE_BUCKET_NAME = ''
    AWS_SERVICE_NAME = ''
    AWS_S3_ENDPOINT_URL = ''
    AWS_S3_FILE_OVERWRITE = ''

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

    KAVENEGAR_API_KEY = ''
    KAVENEGAR_SENDER = '100047778'

    class Config:
        case_sensitive = False
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Config()
