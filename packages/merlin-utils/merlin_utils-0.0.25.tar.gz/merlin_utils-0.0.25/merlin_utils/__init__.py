from .constants import Constants
from .datastore import DatastoreClient
from .publisher import Publisher
from .util import algolia_request, build_statistic_event, emails_substitutions, firebase_auth, validate_email

name = "merlin_utils"


ds_client = DatastoreClient()
constants = Constants()
publisher = Publisher()
