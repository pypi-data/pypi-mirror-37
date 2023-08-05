# -*- coding: utf-8 -*-

"""Main module."""

import json


def jsondiff(first, second):
    """Diff two JSON strings and return JSON with added/changed values."""
    first_dict = json.loads(first)
    second_dict = json.loads(second)
    changed = {}
    # removed = {}
    # changed values
    for key in first_dict.keys() & second_dict.keys():
        if first_dict[key] != second_dict[key]:
            changed[key] = second_dict[key]
    # added values
    for added_key in second_dict.keys() - first_dict.keys():
        changed[added_key] = second_dict[added_key]
    return json.dumps(changed, indent=True)
