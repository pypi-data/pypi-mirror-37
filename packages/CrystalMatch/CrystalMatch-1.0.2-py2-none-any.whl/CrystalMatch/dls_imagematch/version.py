# Version information for CrystalMatch
__version__ = "1.0.2"
__date__ = "26/10/2018"


class VersionHandler:
    def __init__(self):
        pass

    @staticmethod
    def version():
        return __version__

    @staticmethod
    def release_date():
        return __date__

    @staticmethod
    def version_string():
        return '%(prog)s ' + VersionHandler.version() + ', ' + VersionHandler.release_date()
