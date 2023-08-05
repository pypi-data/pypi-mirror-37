=====
Usage
=====

To use flattenit in a project::

    import flattenit

Or::

    from flattenit import flattenit

Then you can use the function ``flattenit`` as follows.
If you used the first import above, use ``flattenit.flattenit``::

    matrix = [[1, 2, 3], [4, 5, 6]]
    new_list = flattenit(matrix)

At this point, ``new_list`` will contain ``[1, 2, 3, 4, 5, 6]``.
