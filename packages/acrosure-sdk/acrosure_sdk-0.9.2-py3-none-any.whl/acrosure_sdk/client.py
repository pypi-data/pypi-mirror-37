import hashlib
import hmac
import base64

from .utils import ( api, is_python3 )
from .application import ApplicationManager
from .product import ProductManager
from .policy import PolicyManager
from .data import DataManager
from .team import TeamManager

class AcrosureClient:
    """
    Represents an Acrosure API client

    ...

    Attributes
    ----------
    application : class
        A class for application api
    product : class
        A class for product api
    policy : class
        A class for policy api
    data : class
        A class for data api
    token : str
        An access token

    Methods
    -------
    call_api( token = token, path = path, data = data )
        Call Acrosure API with corresponding url & current API key.
    """

    def __init__( self, token, application_id = None, product_id = None ):
        """
        Parameters
        ----------
        token : str
            An access token
        application_id : str, optional
            A application id
        product_id : str, optional
            A product id
        """

        self.token = token
        call_api = self.call_api
        # def call_api( path, data = None ):
        #     return api( path, data, self.token )

        self.application = ApplicationManager(id = application_id, call_api = call_api)
        self.product = ProductManager(id = product_id, call_api = call_api)
        self.policy = PolicyManager(id = None, call_api =call_api)
        # self.policy = PolicyManager(call_api = call_api)
        self.data = DataManager(call_api = call_api)
        self.team = TeamManager(call_api = call_api)
    
    def call_api( self, path, data = None ):
        """
        Call Acrosure API with corresponding url & current API key.

        Parameters
        ----------
        path : str
            An API path.
        data : dict
            A data object which is specified by Acrosure.
        """

        return api( path, data, self.token )

    def verify_signature( self, signature, data ):
        """
        Verify signature in webhook event.

        Parameters
        ----------
        signature : str
            A signature received from webhook.
        data : str
            A string of raw data.

        Returns
        ----------
        boolean
            Whether the signature is valid or not.
        """
        if is_python3():
            message = bytes(data, "utf-8")
            secret = bytes(self.token, "utf-8")
        else:
            message = bytes(data.decode('utf-8').encode('utf-8'))
            secret = bytes(self.token.decode('utf-8').encode('utf-8'))
        hash = hmac.new(secret, message, hashlib.sha256)

        expected = hash.hexdigest()

        return signature == expected
