class LazyDeveloperException(Exception):
    def __init__(self, message: str = "Unknown error"):
        super(Exception, self).__init__(message)
        self.message = message

    @staticmethod
    def of_incorrect_format(message: str):
        return LazyDeveloperException(f'Incorrect format: {message}')
