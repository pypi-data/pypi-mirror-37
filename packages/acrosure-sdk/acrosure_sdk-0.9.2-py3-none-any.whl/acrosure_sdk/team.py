class TeamManager:
    """
    Represents an TeamManager. (You most likely shouldn't be accessing this directly, use {@link AcrosureClient#team} instead.)
    """

    def __init__( self, call_api ):
        """
        Parameters
        ----------
        call_api : function
            A function which call Acrosure API.
        """
        self.call_api = call_api
    
    def get_info( self ):
        """
        Get current team info.

        Returns
        -------
        dict
            Current team info.
        """

        try:
            resp = self.call_api("/teams/get-info")
            return resp
        except Exception as err:
            raise err
