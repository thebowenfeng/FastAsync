class AsyncTaskException(Exception):
    def __init__(self, message, func_name):
        super().__init__(message)
        self.func_name = func_name

    def __str__(self):
        return f"An exception occured in '{self.func_name}'. The exception reads: {super().__str__()}"