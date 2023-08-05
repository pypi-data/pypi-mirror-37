class ProductManager:
    """
    Represents a ProductManager. (You most likely shouldn't be accessing this directly, use {@link AcrosureClient#product} instead.)
    """

    def __init__( self, id, call_api ):
        """
        Parameters
        ----------
        id : str
            Current managing product id.
        call_api : function
            A function which call Acrosure API.
        """
        self.call_api = call_api
 
    def get( self, product_id ):
        """
        Get product with specify id or with current id.

        Parameters
        ----------
        product_id : str
            A product id.

        Returns
        -------
        dict
            product.
        """
        try:
            resp = self.call_api("/products/get", {
                "product_id": product_id
            })
            return resp
        except Exception as err:
            raise err

    def list( self, query = {} ):
        """
        Get products list with or without query.
        Parameters
        ----------
        query : dict, optional
            Query object (See Acrosure API document for more detail).

        Returns
        -------
        list
            Products.
        """
        try:
            resp = self.call_api("/products/list", query)
            return resp
        except Exception as err:
            raise err
