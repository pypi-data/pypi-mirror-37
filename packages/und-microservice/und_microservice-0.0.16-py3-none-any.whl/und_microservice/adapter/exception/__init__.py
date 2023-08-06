class NotKeyOptionException(Exception):
    
    """ Excepcion no existe configuraciones  """
    def __init__(self):
        super().__init__(
            'Service not foun or not have onjected in this handler'
        )