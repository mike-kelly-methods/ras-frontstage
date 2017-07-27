"""
This module hosts the config setup for our project
"""

import os

# ENV VARIABLES BELOW, SET THESE ON YOUR TERMINAL
# export APP_SETTINGS=config.Config
# export FLASK_APP=application.py
# export OAUTHLIB_INSECURE_TRANSPORT=1

# Environment variables for running locally using the server.js Node server in ras-backstage-ui)
# To use these stubs:
#   git clone ras-backstage-ui
#   npm install
#   node server.js to run the app on localhost:8050
#
# And set these environment variables on the ras-frontstage terminal:
# export API_GATEWAY_CASE_URL=http://localhost:8050/api/cases/
# export API_GATEWAY_COLLECTION_INSTRUMENT_URL=http://localhost:8050/api/collection-instruments/
# export API_GATEWAY_SURVEYS_URL=http://localhost:8050/api/surveys/
# export API_GATEWAY_AGGREGATED_SURVEYS_URL=http://localhost:8050/api/my-surveys/
# export API_GATEWAY_PARTY_URL=http://localhost:8050/api/party-api/
# export API_GATEWAY_IAC_URL=http://localhost:8050/api/iacs/

# export ONS_OAUTH_SERVER=ras-django-int.apps.devtest.onsclofo.uk
# export ONS_OAUTH_SERVER=ras-django-ci.apps.devtest.onsclofo.uk
# Log is as testuser@email.com , password
# OR
# Log in using your account on:
# export ONS_OAUTH_SERVER=ons-oauth2.cfapps.io


# Default values
if "APP_SETTINGS" not in os.environ:
    os.environ["APP_SETTINGS"] = "config.Config"


class Config(object):
    """
    Base config class
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    # WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    dbname = "ras_frontstage_backup"
    # SQLALCHEMY_DATABASE_URI = "postgresql://" + dbname + ":password@localhost:5431/postgres"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://ras_frontstage_backup:password@localhost:5431/postgres')

    ONS_OAUTH_PROTOCOL = os.environ.get('ONS_OAUTH_PROTOCOL', 'http://')
    ONS_OAUTH_SERVER = os.environ.get('ONS_OAUTH_SERVER', 'ons-oauth2.cfapps.io')
    RAS_FRONTSTAGE_CLIENT_ID = os.environ.get('RAS_FRONTSTAGE_CLIENT_ID', 'ons@ons.gov')
    RAS_FRONTSTAGE_CLIENT_SECRET = os.environ.get('RAS_FRONTSTAGE_CLIENT_SECRET', 'password')
    ONS_AUTHORIZATION_ENDPOINT = os.environ.get('ONS_AUTHORIZATION_ENDPOINT', '/web/authorize/')
    ONS_TOKEN_ENDPOINT = os.environ.get('ONS_TOKEN_ENDPOINT', '/api/v1/tokens/')
    ONS_ADMIN_ENDPOINT = os.environ.get('ONS_ADMIN_ENDPOINT', '/api/account/create')
    
    # Cloud Foundry config

    # TODO - Define default CF endpoints
    API_GATEWAY_CASE_URL = os.environ.get('API_GATEWAY_CASE_URL',
                                          'http://localhost:8050/api/cases/')

    # TODO - Define default CF endpoints
    API_GATEWAY_COLLECTION_EXERCISE_URL = os.environ.get('API_GATEWAY_COLLECTION_EXERCISE_URL',
                                                         'http://localhost:8050/api/collectionexercises/')

    API_GATEWAY_COLLECTION_INSTRUMENT_URL = os.environ.get('API_GATEWAY_COLLECTION_INSTRUMENT_URL',
                                                           'http://ras-api-gateway-int.apps.devtest.onsclofo.uk:80/collection-instrument-api/1.0.2/')
    API_GATEWAY_SURVEYS_URL = os.environ.get('API_GATEWAY_SURVEYS_URL',
                                             'https://ras-api-gateway-int.apps.devtest.onsclofo.uk/api/1.0.0/surveys/')
    API_GATEWAY_AGGREGATED_SURVEYS_URL = os.environ.get('API_GATEWAY_AGGREGATED_SURVEYS_URL',
                                                        'https://ras-api-gateway-int.apps.devtest.onsclofo.uk/api/1.0.0/surveys/')
    API_GATEWAY_PARTY_URL = os.environ.get('API_GATEWAY_PARTY_URL',
                                           'https://ras-api-gateway-int.apps.devtest.onsclofo.uk/party-api/1.0.4/')
    API_GATEWAY_IAC_URL = os.environ.get('API_GATEWAY_IAC_URL',
                                         'https://ras-api-gateway-int.apps.devtest.onsclofo.uk/api/1.0.0/iacs/')
    
    PASSWORD_MATCH_ERROR_TEXT = 'Your passwords do not match'
    PASSWORD_CRITERIA_ERROR_TEXT = 'Your password doesn\'t meet the requirements'
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 160

    #
    #   These settings are to support the new post_event routine which has been ported
    #   into ras-frontstage from ras-common. The style of environment variable over-ride
    #   has been taken from JB's new common code implementation.
    #
    RM_CASE_SERVICE_HOST = os.getenv('RM_CASE_SERVICE_HOST', 'localhost')
    RM_CASE_SERVICE_PORT = os.getenv('RM_CASE_SERVICE_PORT', 8171)
    RM_CASE_SERVICE_PROTOCOL = os.getenv('RM_CASE_SERVICE_PROTOCOL', 'http')
    RM_CASE_SERVICE = '{}://{}:{}/'.format(RM_CASE_SERVICE_PROTOCOL, RM_CASE_SERVICE_HOST, RM_CASE_SERVICE_PORT)

    RAS_COLLECTION_INSTRUMENT_SERVICE_HOST = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_HOST', 'localhost')
    RAS_COLLECTION_INSTRUMENT_SERVICE_PORT = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_PORT', 8002)
    RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL', 'http')
    RAS_COLLECTION_INSTRUMENT_SERVICE = '{}://{}:{}/'.format(RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL, RAS_COLLECTION_INSTRUMENT_SERVICE_HOST, RAS_COLLECTION_INSTRUMENT_SERVICE_PORT)

    RAS_API_GATEWAY_SERVICE_HOST = os.getenv('RAS_API_GATEWAY_SERVICE_HOST', 'localhost')
    RAS_API_GATEWAY_SERVICE_PORT = os.getenv('RAS_API_GATEWAY_SERVICE_PORT', 8080)
    RAS_API_GATEWAY_SERVICE_PROTOCOL = os.getenv('RAS_API_GATEWAY_SERVICE_PROTOCOL', 'http')
    RAS_API_GATEWAY_SERVICE = '{}://{}:{}/'.format(RAS_API_GATEWAY_SERVICE_PROTOCOL, RAS_API_GATEWAY_SERVICE_HOST, RAS_API_GATEWAY_SERVICE_PORT)


class ProductionConfig(Config):
    """
    Production config class
    """
    DEBUG = False


class StagingConfig(Config):
    """
    Staging config class
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development config class
    """
    DEVELOPMENT = True
    DEBUG = True
    
    RAS_FRONTSTAGE_CLIENT_ID = os.environ.get('RAS_FRONTSTAGE_CLIENT_ID', 'ons@ons.gov')
    RAS_FRONTSTAGE_CLIENT_SECRET = os.environ.get('RAS_FRONTSTAGE_CLIENT_SECRET', 'password')


class TestingConfig(Config):
    """
    Testing config class
    """
    TESTING = True
    DEBUG = True
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Local version for OAuth2 server:
    ONS_OAUTH_PROTOCOL = os.environ.get('ONS_OAUTH_PROTOCOL', 'http://')
    ONS_OAUTH_SERVER = os.environ.get('ONS_OAUTH_SERVER', 'localhost:8000')
    RAS_FRONTSTAGE_CLIENT_ID = os.environ.get('RAS_FRONTSTAGE_CLIENT_ID', 'ons@ons.gov')
    RAS_FRONTSTAGE_CLIENT_SECRET = os.environ.get('RAS_FRONTSTAGE_CLIENT_SECRET', 'password')
    ONS_AUTHORIZATION_ENDPOINT = os.environ.get('ONS_AUTHORIZATION_ENDPOINT', '/web/authorize/')
    ONS_TOKEN_ENDPOINT = os.environ.get('ONS_TOKEN_ENDPOINT', '/api/v1/tokens/')
    ONS_ADMIN_ENDPOINT = os.environ.get('ONS_ADMIN_ENDPOINT', '/api/account/create')

    API_GATEWAY_PARTY_URL = os.environ.get('API_GATEWAY_PARTY_URL',
                                           'http://localhost:5201/party-api/v1/')

    # Local version of Collection Instrument Service:
    COLLECTION_INSTRUMENT_URL = os.environ.get('COLLECTION_INSTRUMENT_URL', 'https://api-dev.apps.mvp.onsclofo.uk:443/collection-instrument-api/1.0.2/')

    # Local verions of Survey serivce:
    SURVEYS_URL = os.environ.get('SURVEYS_URL', 'https://api-dev.apps.mvp.onsclofo.uk/api/1.0.0/surveys/')


class OAuthConfig(Config):
    """
    This class is used to configure OAuth2 parameters for the microservice.
    This is temporary until an admin config feature
    is added to allow manual config of the microservice
    """

    ONS_OAUTH_PROTOCOL = os.environ.get('ONS_OAUTH_PROTOCOL', 'https://')
    ONS_OAUTH_SERVER = os.environ.get('ONS_OAUTH_SERVER', 'ons-oauth2.cfapps.io')
    RAS_FRONTSTAGE_CLIENT_ID = os.environ.get('RAS_FRONTSTAGE_CLIENT_ID', 'ons@ons.gov')
    RAS_FRONTSTAGE_CLIENT_SECRET = os.environ.get('RAS_FRONTSTAGE_CLIENT_SECRET', 'password')
    ONS_AUTHORIZATION_ENDPOINT = os.environ.get('ONS_AUTHORIZATION_ENDPOINT', '/web/authorize/')
    ONS_TOKEN_ENDPOINT = os.environ.get('ONS_TOKEN_ENDPOINT', '/api/v1/tokens/')
    ONS_ADMIN_ENDPOINT = os.environ.get('ONS_ADMIN_ENDPOINT', '/api/account/create')


class SecureMessaging(Config):
    """Used to configure Secure Messaging"""

    MESSAGE_LIMIT = 1000

    SM_API_URL = os.environ.get('SM_URL', 'http://localhost:5050')
    SM_UI_URL = os.environ.get('SM_UI_URL', 'http://localhost:5001/secure-message')
    CREATE_MESSAGE_API_URL = SM_API_URL + '/message/send'
    CREATE_MESSAGE_UI_URL = SM_UI_URL + '/create-message'
    MESSAGE_DRAFT_URL = SM_UI_URL + '/DRAFT'
    MESSAGES_API_URL = SM_API_URL + '/messages?limit=' + str(MESSAGE_LIMIT)
    MESSAGE_GET_URL = SM_API_URL + '/message/{0}'
    MESSAGE_MODIFY_URL = SM_API_URL + '/message/{0}/modify'
    MESSAGES_UI_URL = SM_UI_URL + '/messages'
    DRAFT_SAVE_API_URL = SM_API_URL + '/draft/save'
    DRAFT_GET_API_URL = SM_API_URL + '/draft/{0}'
    DRAFT_ID_API_URL = SM_API_URL + '/draft/<draft_id>'
    DRAFT_PUT_API_URL = SM_API_URL + '/draft/{0}/modify'

    # Selenium Driver Path
    chrome_driver = "{}/tests/selenium_scripts/drivers/chromedriver".format(os.environ.get('RAS_FRONTSTAGE_PATH'))
