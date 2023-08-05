__version__ = '0.11.2'


class FondueError(Exception):
    """ Base exception from which all others inherit. """
    pass


class PeeringError(FondueError):
    pass


class ConnectionReset(FondueError):
    pass


class ConfigError(FondueError):
    pass