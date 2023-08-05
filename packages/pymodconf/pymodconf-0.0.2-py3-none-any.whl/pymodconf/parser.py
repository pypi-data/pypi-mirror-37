# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2018 by Lars Klitzke, Lars.Klitzke@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


# Registered tags
from pymodconf import tag
from pymodconf.io import read

__all__ = [
    'InvalidConfigurationError',
    'load',
    'validate',
    'parse'
]


class InvalidConfigurationError(RuntimeError):
    """ Error for an invalid configurations. """
    pass


def load(path, mapping=None):
    """ Load the configuration specified as `path` using the given `mapping`

    Args:
        path (str): Path to the configuration to load.
        mapping (dict[str, list[str]]): A dictionary with required sections and their options.

    Raises:
        InvalidConfigurationError if required sections or options are missing.
    """

    # read the configuration file
    parser = read(path)

    # parse the file
    configuration = parse(parser)

    if mapping:
        # only validate the configuration if a mapping is specified
        validate(configuration, mapping)

    return configuration


def validate(config, mapping):
    """
    Checks if each required section and option is specified in the given `configuration`.

    Args:
        config (dict[str:any|list[any]]): The configuration dictionary
        mapping (dict[str:str]): A dictionary with required sections and their options.

    Raises:
        InvalidConfigurationError: If any required section or option is missing.

    """
    # check if all require options are available
    for section in mapping:
        if section not in config:
            raise InvalidConfigurationError('Section {} is missing'.format(section))

        for option in mapping[section]:
            if option not in config[section]:
                raise InvalidConfigurationError('Option {} not in Section {}'.format(option, section))


def parse(parser):
    """
    Use the config `parser` and generates a dictionary of dictionaries for each section.

    Arguments:
        parser (configparser.ConfigParser): The configuration parser.

    Raises:
        FileNotFoundError: If the specified configuration file cannot be found.

    Returns:
        dict[str:any|list[any]]: The configuration dictionary

    Each section with a registered `tag` found in the configuration file will have a dedicated
    entry in the final dictionary. The key of that section is the name of the tag, see `access()`.
    For instance, all section with the registered tag `Module:` can be found in the dictionary
    with the key `module`. The name of the section can be found using the `name` key.

    All other sections and options names are identical to the names in the configuration file.
    """

    # get the default values of the configuration file
    defaults = parser.defaults()

    config = {}

    # get all available section in the configuration file
    sections = parser.sections()

    if defaults:
        # add defaults to config
        config = {i: parser.get('DEFAULT', i) for i in defaults}

        # split string with , and save as list
        for key, value in config.items():
            if isinstance(value, str) and "," in value:
                config[key] = [v.strip() for v in value.split(",")]

        try:
            # delete the default section
            sections.delete('DEFAULT')
        except AttributeError:
            # no default section available
            pass

    # init config with registered tags
    for t in tag.list():
        config[str(t)] = []

    for sec in sections:

        # init section definition objects get the options for each entry
        section_def = {opt: parser.get(sec, opt) for opt in parser.options(sec)}

        # split string with , and save as list
        for key, value in section_def.items():
            if isinstance(value, str) and "," in value:
                section_def[key] = [v.strip() for v in value.split(",")]

        # check if section has a tag
        sec_tag = None
        for t in tag.list():
            if sec.startswith(t.name):
                sec_tag = t
                break

        if sec_tag:
            # remove the tag, trailing and leading white spaces from the name
            section_def['name'] = sec.replace(sec_tag.name, '').strip()

            config[str(sec_tag)].append(section_def)
        else:
            # just add the section to the configuration
            config[sec] = section_def

    return config
