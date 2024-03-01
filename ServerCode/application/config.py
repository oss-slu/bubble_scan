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

    def set_config_value(self, key, value):
        """
        Set a configuration value.

        :param key: str, the key for the configuration value.
        :param value: any, the value to be set.
        """

        setattr(self, key, value)

    def remove_config_value(self, key):
        """
        Remove a configuration value.

        :param key: str, the key for the configuration value.
        """

        if hasattr(self, key):
            delattr(self, key)


    def get_all_config_values(self):
        """
        Get all configuration values.

        :return: dict, a dictionary containing all configuration values.
        """

        return {key: getattr(self, key) for key in dir(self)
            if not callable(getattr(self, key)) and not key.startswith("__")}


#class ProductionConfig(Config):
    #"""Production configuration"""



#class DevelopmentConfig(Config):
    #"""Development configuration"""

#class TestingConfig(Config):
    #"""Testing configuration"""

    TESTING = True
