### Do *not* commit data and or library files

Feel free to have a text file with links to static hosting of those
files. Let's try to keep this repository small until we are absolutely
sure we are ready.

### Coding standards

##### In general, just follow [PEP 8](http://legacy.python.org/dev/peps/pep-0008/).

If you don't need absolutely need a  class, then don't write a damned
class. Use functions as much as possible.

Since we are writing for Python 2, we should be aware of Python 3 and
try to keep as much as possible portable by 2to3. Notably, use the new
with statement and avoid the print statement in favor of the new print
function.

1. Use the `with` statement:

    from __future__ import with_statement
    with open('input.txt') as f:
        text = f.read()

2. Use the `print()` function:

    from __future__ import print_function
    print('Hi!')

#### File format

All files should be in Unix format in UTF-8.

Each python file should have the following header:

    #!/usr/bin/env python

    """
    Python source code - replace this with a description of the code and
    write the code below this text.
    """

    # vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

    from __future__ import with_statement, print_function

### NO TAB CHARACTERS, EVER.

4 spaces or die.
