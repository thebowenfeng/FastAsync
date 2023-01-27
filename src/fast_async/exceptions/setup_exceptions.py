class PythonVersionError(Exception):
    def __init__(self, message, version):
        super().__init__(message)
        self.version = version

    def __str__(self):
        return f"The minimum Python version this package support is 3.7.0. Your Python version is {self.version[0]}." \
               f"{self.version[1]}.{self.version[2]}"


class RequiredModuleNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.package_name = message

    def __str__(self):
        return f"Cannot import required package '{self.package_name}'. Check that you have '{self.package_name}' " \
               f"installed"
