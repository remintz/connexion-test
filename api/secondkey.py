import datetime
import logging
from connexion import NoContent

log = logging.getLogger(__name__)

def search():
    return NoContent, 202

