# super proto

import klayout.db as kdb
# import pya as kdb

from functools import wraps
from contextlib import contextmanager

from lytest import kqp


@contextmanager
def save_or_visualize(device_name=None, out_file=None):
    ''' Handles a conditional write to file or send over lyipc connection.
        The context manager yields a new empty Device.
        The context block then modifies that device by adding references to it. It does not need to return anything.
        Back to the context manager, the Device is saved if out_file is not None, or it is sent over ipc

        Example::

            with save_or_visualize(out_file='my_box.gds') as D:
                r = D << phidl.geometry.rectangle(size=(10, 10), layer=1)
                r.movex(20)

        will write the device with a rectangle to a file called 'my_box.gds' and do nothing with lyipc.
        By changing out_file to None, it will send an ipc load command instead of writing to a permanent file,
        (Although ipc does write a file to be loaded by klayout, it's name or persistence is not guaranteed.)
    '''
    layout = kdb.Layout()
    layout.dbu = 0.001
    if device_name is None:
        CELL = layout.create_cell('TOP')
    else:
        CELL = layout.create_cell(device_name)
    yield (CELL, layout)
    if out_file is None:
        kqp(CELL, fresh=True)
    else:
        layout.write(out_file)


def contained_geometry(func):
    '''
        Converts a function that takes a Device argument to one that takes a filename argument.
        This is used to develop fixed geometry creation blocks and then save them as reference files.
        Bad idea to try to use this in a library or call it from other functions.

        func should take *only one* argument that is a Device, modify that Device, and return nothing.

        It's sort of a decorator version of save_or_visualize.
        When called with a None argument, it will use klayout_quickplot.

        Example::

            @contained_geometry
            def boxer(D):
                r = D << phidl.geometry.rectangle(size=(10, 10), layer=1)
                r.movex(20)

        Usage::

            boxer()  # displays in klayout over ipc
            boxer('temp.gds')  # saves to file instead

    '''
    @wraps(func)
    def geometry_container(out_file=None):
        with save_or_visualize(out_file=out_file) as stuff:
            TOP, layout = stuff
            func(TOP, layout)
    return geometry_container