Release Notes
=============

0.0.2
-----

Revised package structure to solve module import errors with Sphinx.

Nimbus and Command classes are now imported like this:

.. code-block:: python

    from nimbusinator.nimbus import Nimbus
    from nimbusinator.command import Command

0.0.1
-----

First public release!

Key features:

* High-resolution (640x250) 4 colour mode
* Low-resolution (320x250) 16 colour mode
* Welcome Screen and DOS boot sequence
* Full screen mode
* Nimbus sleep method
* Keyboard input with cursor
* Nimbus colours
* Both Nimbus charsets

Commands added:

* area(coord_list, brush=None)
* ask_charset()
* ask_curpos()
* cursor_position (tuple)
* cls()
* flush()
* gets()
* input(prompt)
* line(coord_list, brush=None)
* plonk_logo(coord)
* plot(text, coord, size=1, brush=None, direction=0, font=None)
* print(text)
* put(ascii_data)
* set_border(colour)
* set_brush(colour)
* set_charset(charset)
* set_colour(colour1, colour2)
* set_curpos(cursor_position)
* set_cursor(flag)
* set_mode(columns)
* set_paper(colour)
* set_pen(colour)