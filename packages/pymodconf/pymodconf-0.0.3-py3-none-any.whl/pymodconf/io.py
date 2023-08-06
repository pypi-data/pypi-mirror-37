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
import configparser
import os

__all__ = [
    'mkdirs',
    'read'
]


def mkdirs(config):
    """
    Create all directories defined in the `config`.

    Args:
        config (dict[str:any|list[any]]): The configuration dictionary

    Notes:
        The option name has to have a '-dir' suffix, e.g. base-dir.

    """
    for section in config:
        for option in config[section]:
            if option.endswith('-dir'):
                directory = os.path.abspath(config[section][option])

                # let makedirs raise exception on any error
                os.makedirs(directory)


def read(file):
    """
    Read the config defined by `file`.

    Arguments:
        file (str): The path of the configuration file.

    Raises:
        FileNotFoundError: If the specified configuration file cannot be found.

    Returns:
        configparser.ConfigParser: Parser initialized with the given file.
    """

    if not os.path.exists(file) or not os.path.isfile(file):
        raise FileNotFoundError("Cannot find configuration file {}".format(file))

    # initialize the configuration parser
    parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

    # parse in the configuration file
    parser.read(file)

    return parser
