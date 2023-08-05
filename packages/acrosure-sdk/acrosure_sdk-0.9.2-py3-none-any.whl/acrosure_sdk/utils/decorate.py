def decorate( obj ):
    try:
        return { k: v for k, v in obj.items() if v is not None }
    except Exception as err:
        raise Exception(err)
