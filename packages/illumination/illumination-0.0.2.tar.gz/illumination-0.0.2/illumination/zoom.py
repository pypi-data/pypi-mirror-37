'''
Tools for adding zoom frames to an illustration.
'''

from .imports import *
from .illustrations import *
from .frames import ZoomFrame, LocalZoomFrame, LocalStampFrame

__all__ = ['add_grid_of_zooms', 'add_zoom', 'add_stamp']


def add_zoom(illustration, position, size=(25, 25), zoom=5, camera='camera'):
    '''
    Add a ZoomFrame to an illustration,
    at roughly its position.

    Parameters
    ----------
    illustration : an Illustration
        This is the overall illustration to which
        we want to be adding a local zoom.
    position : tuple
        (x,y) position of where the zoom should be centered
    size : tuple
        (nrows, ncols) shape of the region to zoom
    zoom : float
        By what factor do we magnify, relative to the original pixels
    camera : str
        Must exist as a key in the illustration.frames
    '''

    # to which frame do we add this?
    reference_frame = illustration.frames[camera]

    # define a key for this frame
    key = 'zoom-{}-({},{})'.format(camera, position[0], position[1])
    illustration.frames[key] = LocalZoomFrame(illustration=illustration,
                                              ax=None,
                                              source=reference_frame,
                                              position=position,
                                              size=size,
                                              zoom=zoom)

    return illustration.frames[key]


def add_grid_of_zooms(illustration, N=4, buffer=100, cameras=[1, 2, 3, 4], zoom=10, size=10, **kw):
    for c in cameras:
        f = illustration.frames['cam{}'.format(c)]

        buffer = size * zoom
        for row in np.linspace(f.ymin + buffer, f.ymax - buffer, N):
            for col in np.linspace(f.xmin + buffer, f.xmax - buffer, N):
                add_zoom(illustration, position=(col, row),
                         camera='cam{}'.format(c), size=size, zoom=zoom, **kw)


def add_stamp(illustration, stamp, zoom=5, camera='camera'):
    '''
    Add a Stamp to an illustration,
    at roughly its position.

    Parameters
    ----------
    illustration : an Illustration
        This is the overall illustration to which
        we want to be adding a local zoom.
    position : tuple
        (x,y) position of where the zoom should be centered
    size : tuple
        (nrows, ncols) shape of the region to zoom
    zoom : float
        By what factor do we magnify, relative to the original pixels
    camera : str
        Must exist as a key in the illustration.frames
    '''

    # to which frame do we add this?
    reference_frame = illustration.frames[camera]
    position = stamp.static['COL_CENT'], stamp.static['ROW_CENT']

    # define a key for this frame
    key = 'stamp-{}-({},{})'.format(camera, position[0], position[1])
    illustration.frames[key] = LocalStampFrame(illustration=illustration,
                                               ax=None,
                                               data=stamp,
                                               source=reference_frame,
                                               position=position,
                                               zoom=zoom)

    return illustration.frames[key]
