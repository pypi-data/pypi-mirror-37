=====
Usage
=====

To use JonTools in a project::

    from jontools import jontools

    a = [
        {'id': 1, 'thing': 2},
        {'id': 2, 'thing': 3}
    ]

    jontools.create_list_index(a)

    #{1: [{'id': 1, 'thing': 2}], 2: [{'id': 2, 'thing': 3}]}
