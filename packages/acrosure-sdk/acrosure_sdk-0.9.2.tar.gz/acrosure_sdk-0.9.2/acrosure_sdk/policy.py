class PolicyManager:
    """
    Represents an PolicyManager. (You most likely shouldn't be accessing this directly, use {@link AcrosureClient#policy} instead.)
    """

    def __init__( self, id, call_api ):
        """
        Parameters
        ----------
        id: str
            A policy id.
        call_api : function
            A function which call Acrosure API.
        """
        self.call_api = call_api

    def get( self, policy_id ):
        """
        Get policy with specify id or with current id.

        Parameters
        ----------
        id : str
            A policy id.

        Returns
        -------
        dict
            Policy.
        """
        try:
            resp = self.call_api("/policies/get", {
                "policy_id": policy_id
            })
            return resp
        except Exception as err:
            raise err
    
    def list( self, query = {} ):
        """
        Get policies list with or without query.
        Parameters
        ----------
        query : dict, optional
            Query object (See Acrosure API document for more detail).

        Returns
        -------
        list
            Policies.
        """
        try:
            resp = self.call_api("/policies/list", query)
            return resp
        except Exception as err:
            raise err
