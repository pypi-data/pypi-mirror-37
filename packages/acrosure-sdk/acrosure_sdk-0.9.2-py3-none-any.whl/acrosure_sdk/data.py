from .utils import decorate

class DataManager:
    """
    Represents an DataManager. (You most likely shouldn't be accessing this directly, use {@link AcrosureClient#data} instead.)
    """

    def __init__( self, call_api ):
        """
        Parameters
        ----------
        call_api : function
            A function which call Acrosure API.
        """
        self.call_api = call_api
    
    def get( self, handler, dependencies = None ):
        """
        Get data from a handler.

        Parameters
        ----------
        handler : str
            A handler string.
        dependencies : list, optional
            An array of dependencies (if needed).

        Returns
        -------
        dict
            Available values for the combination of handler/dependencies.
        """

        try:
            body = decorate({
                "handler": handler,
                "dependencies": dependencies,
            })
            resp = self.call_api("/data/get", body)
            return resp
        except Exception as err:
            raise err
