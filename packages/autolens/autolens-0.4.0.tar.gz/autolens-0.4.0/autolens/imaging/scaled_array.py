import logging

import numpy as np

from autolens.imaging import imaging_util

logging.basicConfig()
logger = logging.getLogger(__name__)


class Array(np.ndarray):

    def __new__(cls, array, *args, **kwargs):
        return np.array(array, dtype='float64').view(cls)

    def __reduce__(self):
        # Get the parent's __reduce__ tuple
        pickled_state = super(Array, self).__reduce__()
        # Create our own tuple to pass to __setstate__
        class_dict = {}
        for key, value in self.__dict__.items():
            class_dict[key] = value
        new_state = pickled_state[2] + (class_dict,)
        # Return a tuple that replaces the parent's __setstate__ tuple with our own
        return pickled_state[0], pickled_state[1], new_state

    # noinspection PyMethodOverriding
    def __setstate__(self, state):

        for key, value in state[-1].items():
            setattr(self, key, value)
        super(Array, self).__setstate__(state[0:-1])

    def trim_around_centre(self, new_shape):
        """Trim the array to a new shape.
        
        Parameters
        -----------
        new_shape : (int, int)
            The new two-dimensional shape of the array.
        """
        return self.new_with_array(imaging_util.trim_array_2d_around_centre(self, new_shape))

    def trim_around_region(self, x0, x1, y0, y1):
        """Trim the array to a new shape.

        Parameters
        -----------
        new_shape : (int, int)
            The new two-dimensional shape of the array.
        """
        return self.new_with_array(imaging_util.trim_array_2d_around_region(self, x0, x1, y0, y1))

    def new_with_array(self, array):
        """
        Parameters
        ----------
        array: ndarray
            An ndarray

        Returns
        -------
        new_array: ScaledSquarePixelArray
            A new instance of this class that shares all of this instances attributes with a new ndarray.
        """
        arguments = vars(self)
        arguments.update({"array": array})

        return self.__class__(**arguments)

    @classmethod
    def from_fits_with_scale(cls, file_path, hdu):
        """
        Loads the data from a .fits file.

        Parameters
        ----------
        file_path : str
            The full path of the fits file.
        hdu : int
            The HDU number in the fits file containing the _image data.
        pixel_scales: float
            The arc-second to pixel conversion factor of each pixel.
        """
        return cls(imaging_util.numpy_array_from_fits(file_path, hdu))


class ScaledArray(Array):

    # noinspection PyUnusedLocal
    def __init__(self, array):
        """
        Parameters
        ----------
        array: ndarray
            An array representing data (e.g. an _image, noise-mappers, etc.)
        pixel_scales: float
            The arc-second to pixel conversion factor of each pixel.
        """
        # noinspection PyArgumentList
        super(ScaledArray, self).__init__()

    def map(self, func):
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                func(x, y)

    @property
    def central_pixel_coordinates(self):
        """
        Returns
        -------
        central_pixel_coordinates:
            The coordinates of the central pixel in the _image. If a dimension of the _image are odd then the \
            corresponding coordinate will be fractional values in the centre.
        """
        return float(self.shape[0] - 1) / 2, float(self.shape[1] - 1) / 2

    @property
    def xticks(self):
        """Compute the xticks labels of this grid, used for plotting the x-axis ticks when visualizing an _image-grid"""
        return np.linspace(-self.shape_arc_seconds[1] / 2.0, self.shape_arc_seconds[1] / 2.0, 4)

    @property
    def yticks(self):
        """Compute the yticks labels of this grid, used for plotting the y-axis ticks when visualizing an _image-grid"""
        return np.linspace(-self.shape_arc_seconds[0] / 2.0, self.shape_arc_seconds[0] / 2.0, 4)


class ScaledSquarePixelArray(ScaledArray):
    """
    Class storing the grids for 2D pixel grids (e.g. _image, PSF, signal_to_noise_ratio).
    """

    # noinspection PyUnusedLocal
    def __init__(self, array, pixel_scale):
        """
        Parameters
        ----------
        array: ndarray
            An array representing data (e.g. an _image, noise-mappers, etc.)
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        """
        # noinspection PyArgumentList
        super(ScaledSquarePixelArray, self).__init__(array=array)
        self.pixel_scale = pixel_scale

    @property
    def pixel_scales(self):
        return (self.pixel_scale, self.pixel_scale)

    def __array_finalize__(self, obj):
        if isinstance(obj, ScaledSquarePixelArray):
            self.pixel_scale = obj.pixel_scale

    @classmethod
    def from_fits_with_scale(cls, file_path, hdu, pixel_scale):
        """
        Loads the data from a .fits file.

        Parameters
        ----------
        file_path : str
            The full path of the fits file.
        hdu : int
            The HDU number in the fits file containing the _image data.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        """
        return cls(imaging_util.numpy_array_from_fits(file_path, hdu), pixel_scale)

    @classmethod
    def single_value(cls, value, shape, pixel_scale):
        """
        Creates an instance of Array and fills it with a single value

        Parameters
        ----------
        value: float
            The value with which the array should be filled
        shape: (int, int)
            The shape of the array
        pixel_scale: float
            The scale of a pixel in arc seconds

        Returns
        -------
        array: ScaledSquarePixelArray
            An array filled with a single value
        """
        array = np.ones(shape) * value
        return cls(array, pixel_scale)

    def pixels_to_arc_seconds(self, pixels):
        """Converts coordinate values from pixels to arc seconds."""
        return self.pixel_scale * pixels

    @property
    def shape_arc_seconds(self):
        """The shape of the _image in arc seconds"""
        return tuple(map(lambda d: self.pixels_to_arc_seconds(d), self.shape))

    def arc_seconds_to_pixels(self, arc_seconds):
        """Converts coordinate values from arc seconds to pixels."""
        return arc_seconds / self.pixel_scale

    def grid_pixels_to_grid_arcseconds(self, grid_pixels):
        """ Converts a grid in coordinates of pixels to a grid in arc seconds.

        The pixel coordinate origin is at the top left corner of an image, whilst the arc-second coordinate origin \
        is at the centre start with negative x and y values from the top-left.

        This means that the top-left pixel coordinates, [0, 0], will give negative arc second coordinates.

        Parameters
        ----------
        grid_pixels : ndarray
            The grid of (x,y) coordinates in units of pixels
        """
        return self.pixel_scale * (grid_pixels - self.central_pixel_coordinates)

    def grid_arc_seconds_to_grid_pixels(self, grid_arc_seconds):
        """
        Converts an arc second coordinate pair to a pixel coordinate pair.

        The pixel coordinate origin is at the top left corner of an image, whilst the arc-second coordinate origin \
        is at the centre start with negative x and y values from the top-left.

        This means that the top-left pixel coordinates, [0, 0], will give negative arc second coordinates.

        Parameters
        ----------
        grid_arc_seconds: ndarray
            The grid of (x,y) coordinates in arc seconds.
        """
        return (grid_arc_seconds / self.pixel_scale) + self.central_pixel_coordinates

    def flatten(self, order='C'):
        """
        Returns
        -------
        flat_scaled_array: ScaledSquarePixelArray
            A copy of this array flattened to 1D
        """
        return self.new_with_array(super(ScaledSquarePixelArray, self).flatten(order))

    def sub_pixel_to_coordinate(self, sub_pixel, arcsec, sub_grid_size):
        """Convert a sub-pixel coordinate in an _image-pixel to a sub-coordinate, using the pixel scale sub_grid_size."""

        half = self.pixel_scale / 2
        step = self.pixel_scale / (sub_grid_size + 1)

        return arcsec - half + (sub_pixel + 1) * step

    @property
    def grid_2d(self):
        """ The arc second-grid of (x,y) coordinates of every pixel.

        This is defined from the top-left corner, such that the first pixel at location [0, 0] will have a negative x \
        value y value in arc seconds.
        """
        return imaging_util.image_grid_2d_from_shape_and_pixel_scales(self.shape, self.pixel_scales)

    def __eq__(self, other):
        super_result = super(ScaledSquarePixelArray, self).__eq__(other)
        try:
            return super_result.all()
        except AttributeError:
            return super_result


class ScaledRectangularPixelArray(ScaledArray):
    """
    Class storing the grids for 2D pixel grids (e.g. _image, PSF, signal_to_noise_ratio).
    """

    # noinspection PyUnusedLocal
    def __init__(self, array, pixel_scales):
        """
        Parameters
        ----------
        array: ndarray
            An array representing data (e.g. an _image, noise-mappers, etc.)
        pixel_scales : (float, float)
            The arc-second to pixel conversion factor of each pixel.
        """
        # noinspection PyArgumentList
        super(ScaledRectangularPixelArray, self).__init__(array=array)
        self.pixel_scales = pixel_scales

    def __array_finalize__(self, obj):
        if isinstance(obj, ScaledRectangularPixelArray):
            self.pixel_scales = obj.pixel_scales

    @classmethod
    def from_fits_with_scale(cls, file_path, hdu, pixel_scales):
        """
        Loads the data from a .fits file.

        Parameters
        ----------
        file_path : str
            The full path of the fits file.
        hdu : int
            The HDU number in the fits file containing the _image data.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        """
        return cls(imaging_util.numpy_array_from_fits(file_path, hdu), pixel_scales)

    @classmethod
    def single_value(cls, value, shape, pixel_scales):
        """
        Creates an instance of Array and fills it with a single value

        Parameters
        ----------
        value: float
            The value with which the array should be filled
        shape: (int, int)
            The shape of the array
        pixel_scale: float
            The scale of a pixel in arc seconds

        Returns
        -------
        array: ScaledSquarePixelArray
            An array filled with a single value
        """
        array = np.ones(shape) * value
        return cls(array, pixel_scales)

    def x_pixels_to_arc_seconds(self, pixels):
        """Converts coordinate values from pixels to arc seconds."""
        return self.pixel_scales[0] * pixels

    def y_pixels_to_arc_seconds(self, pixels):
        """Converts coordinate values from pixels to arc seconds."""
        return self.pixel_scales[1] * pixels

    def x_arc_seconds_to_pixels(self, arc_seconds):
        """Converts coordinate values from arc seconds to pixels."""
        return arc_seconds / self.pixel_scales[0]

    def y_arc_seconds_to_pixels(self, arc_seconds):
        """Converts coordinate values from arc seconds to pixels."""
        return arc_seconds / self.pixel_scales[1]

    @property
    def shape_arc_seconds(self):
        """The shape of the _image in arc seconds"""
        return (self.x_pixels_to_arc_seconds(pixels=self.shape[0]), self.y_pixels_to_arc_seconds(pixels=self.shape[1]))

    def grid_pixels_to_grid_arcseconds(self, grid_pixels):
        """ Converts a grid in coordinates of pixels to a grid in arc seconds.

        The pixel coordinate origin is at the top left corner of an image, whilst the arc-second coordinate origin \
        is at the centre start with negative x and y values from the top-left.

        This means that the top-left pixel coordinates, [0, 0], will give negative arc second coordinates.

        Parameters
        ----------
        grid_pixels : ndarray
            The grid of (x,y) coordinates in units of pixels
        """
        return self.pixel_scales * (grid_pixels - self.central_pixel_coordinates)

    def grid_arc_seconds_to_grid_pixels(self, grid_arc_seconds):
        """
        Converts an arc second coordinate pair to a pixel coordinate pair.

        The pixel coordinate origin is at the top left corner of an image, whilst the arc-second coordinate origin \
        is at the centre start with negative x and y values from the top-left.

        This means that the top-left pixel coordinates, [0, 0], will give negative arc second coordinates.

        Parameters
        ----------
        grid_arc_seconds: ndarray
            The grid of (x,y) coordinates in arc seconds.
        """
        return (grid_arc_seconds / self.pixel_scales) + self.central_pixel_coordinates

    def flatten(self, order='C'):
        """
        Returns
        -------
        flat_scaled_array: ScaledSquarePixelArray
            A copy of this array flattened to 1D
        """
        return self.new_with_array(super(ScaledSquarePixelArray, self).flatten(order))

    def sub_pixel_to_coordinate(self, sub_pixel, arcsec, sub_grid_size):
        """Convert a sub-pixel coordinate in an _image-pixel to a sub-coordinate, using the pixel scale sub_grid_size."""

        half = self.pixel_scales / 2
        step = self.pixel_scales / (sub_grid_size + 1)

        return arcsec - half + (sub_pixel + 1) * step

    @property
    def grid_2d(self):
        """ The arc second-grid of (x,y) coordinates of every pixel.

        This is defined from the top-left corner, such that the first pixel at location [0, 0] will have a negative x \
        value y value in arc seconds.
        """
        return imaging_util.image_grid_2d_from_shape_and_pixel_scales(self.shape, self.pixel_scales)

    def __eq__(self, other):
        super_result = super(ScaledRectangularPixelArray, self).__eq__(other)
        try:
            return super_result.all()
        except AttributeError:
            return super_result