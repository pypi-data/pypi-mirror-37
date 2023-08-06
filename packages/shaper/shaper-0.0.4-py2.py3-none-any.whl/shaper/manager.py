#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""shaper manager - manage library"""
from __future__ import print_function

import fnmatch
import os

from collections import OrderedDict

from shaper import lib
from shaper.lib.configi import FILE_TYPES


def walk_on_path(path):
    """recursive find files with pattern"""
    for root, _dirnames, files in os.walk(path):
        for pattern in FILE_TYPES:
            for filename in fnmatch.filter(files, '*{}'.format(pattern)):
                yield os.path.join(root, filename)


def read_properties(path_to_dir):
    """interface for recursive read properties"""
    return {
        filename: lib.read(filename) for filename in walk_on_path(path_to_dir)
    }


def create_folders(path_to_folder):
    """recursive creating folders"""
    try:
        os.makedirs(path_to_folder)
    except OSError:
        if not os.path.isdir(path_to_folder):
            raise EOFError


def write_properties(datastructure, out_path):
    """interface for recursive write properties"""
    for filename, properties in datastructure.items():
        directories = os.path.join(
            out_path,
            os.path.dirname(filename)
        )
        create_folders(directories)

        property_file = os.path.basename(filename)
        lib.write(
            os.path.join(directories, property_file),
            properties,
        )


def forward_path_parser(_input):
    """
    parsing plain dict to nested.
    """

    def get_or_create_by_key(key, current_tree):
        """update dict by key"""
        if key not in current_tree:
            last = keys.pop()
            # pylint: disable=undefined-loop-variable
            # this value defined !
            dict_update = {last: value}

            for _key in reversed(keys):
                dict_update = {_key: dict_update}

            current_tree.update(dict_update)
        else:
            keys.pop(0)
            get_or_create_by_key(keys[0], current_tree[key])

    output = {}
    for key, value in OrderedDict(_input).items():
        keys = key.split('/')

        get_or_create_by_key(keys[0], output)

    return output


def backward_path_parser(_input):
    """
    make nested structure plain.
    """

    def path_builder(current_tree, key=''):
        """make plain"""
        for _key, _value in current_tree.items():
            _key = key + '/' + _key if key else _key
            if '.' in _key:
                output.update({_key: _value})
            else:
                path_builder(_value, _key)

    output = OrderedDict()
    path_builder(_input)

    return output
