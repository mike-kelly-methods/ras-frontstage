import logging
import requests

from flask import current_app as app
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def current_banner():
    logger.info('Attempting to retrieve the current live banner')
    url = f"{app.config['BANNER_SERVICE_URL']}/banner"
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code != 404:
            logger.error('Failed to retrieve Banner from api')
        return ""

    logger.info('Successfully retrieved current live banner from api')
    if response.status_code == 204:
        return ""
    banner = response.json()
    content = banner.get('content', "")
    return content
