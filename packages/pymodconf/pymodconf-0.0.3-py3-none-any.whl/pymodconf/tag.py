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
# along with this program. If not, see <https://www.gnu.org/licenses/>..

__all__ = [
    'Tag',
    'register',
    'available',
    'list'
]

# Registered tags
_TAGS = []


class Tag(object):
    """
    A `Tag` is configuration section identifier to group specific sections.

    Every tag in the configuration file is assumed to be in the Form of "<Name>:". This class represents such a tag
    and abstracts the usage of the tag in the application. Therefore, it provides an abstraction layer to generate
    a rectified version of the tag for accessing all sections in the configuration with a specific tag.

    """

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name.replace(':', '').strip().lower()

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def name(self):
        """
        Retrieve the original tag name as defined in the configuration file.

        Returns:
            str: The original name of the `Tag`.

        """
        return self._name


def register(tag):
    """
    Register a new tag.

    Args:
        tag (Tag): Tag to register
    """
    if tag:
        global _TAGS

        if tag not in _TAGS:
            _TAGS.append(tag)


def available(tag):
    """
    Checks if the given `tag` was registered:

    Args:
        tag (str|Tag): The tag to check for.

    Returns:
        bool: True if the tag is registered or False otherwise.

    """
    if isinstance(tag, str):
        tag = Tag(tag)

    global _TAGS
    return tag in _TAGS


def list():
    """
    Return the registered `Tag`s.

    Yields:
        Tag: The registered tags
    """
    global _TAGS

    for t in _TAGS:
        yield t
