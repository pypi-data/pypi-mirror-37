from six.moves import configparser
import os.path
import logging

logger = logging.getLogger(__name__)

PROFILE_PREFIX = 'profile:'


class LocalConf(object):
    """
    Manages local configuration for current user.
    Allows multiple configuration profiles.
    """
    def __init__(self, path=None):
        """
        :param path str: Path to a INI configuration file that holds Arkindex settings.
            Defaults to ``~/.arkindex.ini``.
        """
        self.path = path or os.path.join(os.path.expanduser('~'), '.arkindex.ini')
        """Configuration file path"""

        # Read initial configuration
        self.config = self.read()
        """Cached configuration data from the INI file."""

        # Load current profiles
        self.profiles = {
            section[len(PROFILE_PREFIX):]: dict(self.config.items(section))
            for section in self.config.sections()
            if section.startswith(PROFILE_PREFIX)
        }
        """Available configuration profiles."""

    def read(self):
        """
        Read configuration data from the INI file.
        :return: A loaded ConfigParser.
        :rtype: configparser.ConfigParser
        """
        config = configparser.ConfigParser()
        if os.path.exists(self.path):
            logger.debug('Reading configuration {}'.format(self.path))
            config.read(self.path)

        return config

    def write(self):
        """
        Write configuration data to the INI file.
        """
        with open(self.path, 'w') as f:
            self.config.write(f)

    def save_profile(self, profile_name, **kwargs):
        r"""
        Save profile configuration to the in-memory configuration.
        Does not write to the INI file.

        :param profile_name str: Name of the profile to store.
        :param \**kwargs: Configuration data for the profile.
        """
        section = PROFILE_PREFIX + profile_name
        try:
            self.config.add_section(section)
        except configparser.DuplicateSectionError:
            pass
        for name, value in kwargs.items():
            self.config.set(section, name, value)
        self.profiles[profile_name] = kwargs
