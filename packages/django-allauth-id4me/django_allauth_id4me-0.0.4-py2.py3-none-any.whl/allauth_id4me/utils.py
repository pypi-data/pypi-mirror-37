import base64
import pickle

from allauth.compat import UserDict
from .models import ID4meStore

class JSONSafeSession(UserDict):
    """
    openid puts e.g. class OpenIDServiceEndpoint in the session.
    Django 1.6 no longer pickles stuff, so we'll need to do some
    hacking here...
    """
    def __init__(self, session):
        UserDict.__init__(self)
        self.data = session

    def __setitem__(self, key, value):
        data = base64.b64encode(pickle.dumps(value)).decode('ascii')
        return UserDict.__setitem__(self, key, data)

    def __getitem__(self, key):
        data = UserDict.__getitem__(self, key)
        return pickle.loads(base64.b64decode(data.encode('ascii')))

def getRegisteredClient(authority):
    stored_auth = ID4meStore.objects.filter(
        authority=authority
    )

    if stored_auth.count() == 0:
        raise KeyError('Authority not found: {}'.format(authority))

    return_val = None

    return stored_auth[0].context


def storeRegisteredClient(authority, serializedcontext):
    """

    :param authority: authority label
    :type authority str:
    :param context: ID4me context
    :type context: id4me_rp_client.ID4meContext
    """
    ID4meStore.objects.create(
        authority=authority,
        context=serializedcontext)
