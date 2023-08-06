import configparser

"""
global/singleton config object to be uses across modules
"""
config = configparser.ConfigParser()
config.read('config.ini')


def verify_required_options(section, option_keys):
    """
    Verifies that section exists, and that it has option_keys defined
    :param section: Section in the config
    :param option_keys: list of required options
    :type section: str
    :type option_keys: list
    :return: SectionProxy
    """
    if section not in config:
        raise configparser.NoSectionError(section)
    for option in option_keys:
        if option not in config[section]:
            raise configparser.NoOptionError(option, section)
    return config[section]
