=====
Usage
=====

To use Simple JSONDiff in a project::

    >>> from simple_jsondiff import jsondiff
    >>> print(jsondiff('{"a": 1, "b": 3}', '{"a": 2, "b": 3, "c": 4}'))
    {
    "a": 2,
    "c": 4
    }

By default, jsondiff will show all values that are added or changed.
