"""
Module docstring goes here
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    """Base configuration"""

    def get_config_value(self, key, default=None):
        """
        Get a configuration value.

        :param key: str, the key for the configuration value.
        :param default: any, the default value if the key is not found.
        :return: any, the configuration value or the default value.
        """
        return getattr(self, key, default)


#class ProductionConfig(Config):
    #"""Production configuration"""



#class DevelopmentConfig(Config):
    #"""Development configuration"""

#class TestingConfig(Config):
    #"""Testing configuration"""

    TESTING = True
