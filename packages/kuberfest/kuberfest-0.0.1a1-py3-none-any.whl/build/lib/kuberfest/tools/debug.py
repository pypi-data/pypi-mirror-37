class Debug:
    DEBUG_LEVEL_INFO = 'INFO'
    DEBUG_LEVEL_ERROR = 'ERROR'
    DEBUG_LEVEL_EXCEPTION = 'EXCEPTION'

    @staticmethod
    def debug(message='', data=None, debug_level=None):
        if data is None:
            data = {}
        if debug_level is None:
            debug_level = 'INFO'

        print(
            ">>> {debug_level}: {message}".format(
                debug_level=debug_level,
                message=message
            )
        )

    @staticmethod
    def info(message='', data=None):
        return Debug.debug(message, data, Debug.DEBUG_LEVEL_INFO)
    
    @staticmethod
    def error(message='', data=None):
        return Debug.debug(message, data, Debug.DEBUG_LEVEL_ERROR)
    
    @staticmethod
    def exception(message='', data=None):
        return Debug.debug(message, data, Debug.DEBUG_LEVEL_EXCEPTION)
