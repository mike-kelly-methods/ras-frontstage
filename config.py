import os


# To choose which config to use when running frontstage set environment variable APP_SETTINGS to the name of the
# config object e.g. for the dev config set APP_SETTINGS=DevelopmentConfig
class Config(object):
    DEBUG = False
    TESTING = False
    VERSION = '0.2.3'
    PORT = os.getenv('PORT', 8082)
    MAX_UPLOAD_LENGTH = os.getenv('MAX_UPLOAD_LENGTH', 20 * 1024 * 1024)

    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_SECRET = os.getenv('JWT_SECRET')
    VALIDATE_JWT = os.environ.get('VALIDATE_JWT', True)
    GOOGLE_ANALYTICS = os.getenv('GOOGLE_ANALYTICS', None)
    SELENIUM_TEST_URL = os.environ.get('SELENIUM_TEST_URL', 'http://localhost:8080')
    NON_DEFAULT_VARIABLES = ['SECRET_KEY', 'SECURITY_USER_NAME', 'SECURITY_USER_PASSWORD', 'JWT_SECRET']

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', 1)

    PASSWORD_MATCH_ERROR_TEXT = 'Your passwords do not match'
    PASSWORD_CRITERIA_ERROR_TEXT = 'Your password doesn\'t meet the requirements'
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 160

    RAS_FRONTSTAGE_API_HOST = os.getenv('RAS_FRONTSTAGE_API_HOST', 'localhost')
    RAS_FRONTSTAGE_API_PORT = os.getenv('RAS_FRONTSTAGE_API_PORT', 8083)
    RAS_FRONTSTAGE_API_PROTOCOL = os.getenv('RAS_FRONTSTAGE_API_PROTOCOL', 'http')
    RAS_FRONTSTAGE_API_SERVICE = '{}://{}:{}/'.format(RAS_FRONTSTAGE_API_PROTOCOL,
                                                      RAS_FRONTSTAGE_API_HOST,
                                                      RAS_FRONTSTAGE_API_PORT)

    RAS_SECURE_MESSAGE_SERVICE_PROTOCOL = os.getenv('RAS_SECURE_MESSAGING_PROTOCOL', 'http')
    RAS_SECURE_MESSAGE_SERVICE_HOST = os.getenv('RAS_SECURE_MESSAGING_HOST', 'localhost')
    RAS_SECURE_MESSAGE_SERVICE_PORT = os.getenv('RAS_SECURE_MESSAGING_PORT', 5050)

    RAS_SECURE_MESSAGING_SERVICE = '{}://{}:{}/'.format(RAS_SECURE_MESSAGE_SERVICE_PROTOCOL,
                                                        RAS_SECURE_MESSAGE_SERVICE_HOST,
                                                        RAS_SECURE_MESSAGE_SERVICE_PORT)

    GET_MESSAGES_URL = 'secure-messaging/messages-list'
    GET_MESSAGE_URL = 'secure-messaging/message'
    SEND_MESSAGE_URL = 'secure-messaging/send-message'

    SIGN_IN_URL = 'sign-in'

    REQUEST_PASSWORD_CHANGE = 'passwords/request-password-change'
    VERIFY_PASSWORD_TOKEN = 'passwords/verify-password-token'
    CHANGE_PASSWORD = 'passwords/change-password'

    VALIDATE_ENROLMENT = 'register/validate-enrolment'
    CONFIRM_ORGANISATION_SURVEY = 'register/confirm-organisation-survey'
    CREATE_ACCOUNT = 'register/create-account'
    VERIFY_EMAIL = 'register/verify-email'

    SURVEYS_LIST = 'surveys/surveys-list'
    ACCESS_CASE = 'surveys/access-case'
    DOWNLOAD_CI = 'surveys/download-ci'
    UPLOAD_CI = 'surveys/upload-ci'
    ADD_SURVEY = 'surveys/add-survey'
    CONFIRM_ADD_ORGANISATION_SURVEY = 'surveys/add-survey/confirm-add-organisation-survey'
    GENERATE_EQ_URL = 'surveys/generate-eq-url'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'ONS_DUMMY_KEY')
    JWT_SECRET = os.getenv('JWT_SECRET', 'testsecret')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'admin')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'secret')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)


class TestingConfig(DevelopmentConfig):
    TESTING = True
    DEVELOPMENT = False
    WTF_CSRF_ENABLED = False
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    JWT_SECRET = 'testsecret'
    REDIS_DB = os.getenv('REDIS_DB', 13)
