from __future__ import absolute_import, division, print_function

import logging
import warnings

import numpy as np
import pandas as pd

from glue.core.subset import (RoiSubsetState, RangeSubsetState,
                              CategoricalROISubsetState, AndState,
                              CategoricalMultiRangeSubsetState,
                              CategoricalROISubsetState2D)
from glue.core.roi import (PolygonalROI, CategoricalROI, RangeROI, XRangeROI,
                           YRangeROI, RectangularROI)
from glue.core.util import row_lookup
from glue.utils import (unique, shape_to_string, coerce_numeric, check_sorted,
                        polygon_line_intersections, broadcast_to)


__all__ = ['Component', 'DerivedComponent', 'CategoricalComponent',
           'CoordinateComponent']


class Component(object):

    """ Stores the actual, numerical information for a particular quantity

    Data objects hold one or more components, accessed via
    ComponentIDs. All Components in a data set must have the same
    shape and number of dimensions

    Notes
    -----
    Instead of instantiating Components directly, consider using
    :meth:`Component.autotyped`, which chooses a subclass most appropriate
    for the data type.
    """

    def __init__(self, data, units=None):
        """
        :param data: The data to store
        :type data: :class:`numpy.ndarray`

        :param units: Optional unit label
        :type units: str
        """

        # The physical units of the data
        self.units = units

        # The actual data
        # subclasses may pass non-arrays here as placeholders.
        if isinstance(data, np.ndarray):
            data = coerce_numeric(data)
            data.setflags(write=False)  # data is read-only

        self._data = data

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value is None:
            self._units = ''
        else:
            self._units = str(value)

    @property
    def data(self):
        """ The underlying :class:`numpy.ndarray` """
        return self._data

    @property
    def shape(self):
        """ Tuple of array dimensions """
        return self._data.shape

    @property
    def ndim(self):
        """ The number of dimensions """
        return len(self._data.shape)

    def __getitem__(self, key):
        logging.debug("Using %s to index data of shape %s", key, self.shape)
        return self._data[key]

    @property
    def numeric(self):
        """
        Whether or not the datatype is numeric
        """
        # We need to be careful here to not just access self.data since that
        # would force the computation of the whole component in the case of
        # derived components, so instead we specifically only get the first
        # element.
        return np.can_cast(self[(0,) * self.ndim].dtype, np.complex)

    @property
    def categorical(self):
        """
        Whether or not the datatype is categorical
        """
        return False

    @property
    def datetime(self):
        """
        Whether or not or not the datatype is a date/time
        """
        return False

    def __str__(self):
        return "%s with shape %s" % (self.__class__.__name__, shape_to_string(self.shape))

    def jitter(self, method=None):
        raise NotImplementedError

    def subset_from_roi(self, att, roi, other_comp=None, other_att=None, coord='x'):
        """
        Create a SubsetState object from an ROI.

        This encapsulates the logic for creating subset states with Components.
        See the documentation for CategoricalComponents for caveats involved
        with mixed-type plots.

        :param att: attribute name of this Component
        :param roi: an ROI object
        :param other_comp: The other Component for 2D ROIs
        :param other_att: The attribute name of the other Component
        :param coord: The orientation of this Component
        :param is_nested: True if this was passed from another Component.
        :return: A SubsetState (or subclass) object
        """

        if coord not in ('x', 'y'):
            raise ValueError('coord should be one of x/y')

        other_coord = 'y' if coord == 'x' else 'x'

        if isinstance(roi, RangeROI):

            # The selection is either an x range or a y range

            if roi.ori == coord:

                # The selection applies to the current component
                lo, hi = roi.range()
                subset_state = RangeSubsetState(lo, hi, att)

            else:

                # The selection applies to the other component, so we delegate
                return other_comp.subset_from_roi(other_att, roi,
                                                  other_comp=self,
                                                  other_att=att,
                                                  coord=other_coord)

        else:

            # The selection is polygon-like. Categorical components require
            # special care, so if the other component is categorical, we need to
            # delegate to CategoricalComponent.subset_from_roi.

            if isinstance(other_comp, CategoricalComponent):

                return other_comp.subset_from_roi(other_att, roi,
                                                  other_comp=self,
                                                  other_att=att,
                                                  is_nested=True,
                                                  coord=other_coord)
            else:

                subset_state = RoiSubsetState()
                subset_state.xatt = att
                subset_state.yatt = other_att
                x, y = roi.to_polygon()
                subset_state.roi = PolygonalROI(x, y)

        return subset_state

    def to_series(self, **kwargs):
        """ Convert into a pandas.Series object.

        :param kwargs: All kwargs are passed to the Series constructor.
        :return: pandas.Series
        """

        return pd.Series(self.data.ravel(), **kwargs)

    @classmethod
    def autotyped(cls, data, units=None):
        """
        Automatically choose between Component and CategoricalComponent,
        based on the input data type.

        :param data: The data to pack into a Component (array-like)
        :param units: Optional units
        :type units: str

        :returns: A Component (or subclass)
        """
        data = np.asarray(data)

        if np.issubdtype(data.dtype, np.object_):
            return CategoricalComponent(data, units=units)

        if data.dtype.kind == 'M':
            return DateTimeComponent(data)

        n = coerce_numeric(data)

        thresh = 0.5
        try:
            use_categorical = np.issubdtype(data.dtype, np.character) and \
                np.isfinite(n).mean() <= thresh
        except TypeError:  # isfinite not supported. non-numeric dtype
            use_categorical = True

        if use_categorical:
            return CategoricalComponent(data, units=units)
        else:
            return Component(n, units=units)


class DerivedComponent(Component):

    """ A component which derives its data from a function """

    def __init__(self, data, link, units=None):
        """
        :param data: The data object to use for calculation
        :type data: :class:`~glue.core.data.Data`

        :param link: The link that carries out the function
        :type link: :class:`~glue.core.component_link.ComponentLink`

        :param units: Optional unit description
        """
        super(DerivedComponent, self).__init__(data, units=units)
        self._link = link

    def set_parent(self, data):
        """ Reassign the Data object that this DerivedComponent operates on """
        self._data = data

    @property
    def data(self):
        """ Return the numerical data as a numpy array """
        return self._link.compute(self._data)

    @property
    def link(self):
        """ Return the component link """
        return self._link

    def __getitem__(self, key):
        return self._link.compute(self._data, key)


class CoordinateComponent(Component):
    """
    Components associated with pixel or world coordinates

    The numerical values are computed on the fly.
    """

    def __init__(self, data, axis, world=False):
        super(CoordinateComponent, self).__init__(None, None)
        self.world = world
        self._data = data
        self.axis = axis

    @property
    def data(self):
        return self._calculate()

    def _calculate(self, view=None):

        if self.world:

            # Calculating the world coordinates can be a bottleneck if we aren't
            # careful, so we need to make sure that if not all dimensions depend
            # on each other, we use smart broadcasting.

            # The unoptimized way to do this for an N-dimensional dataset would
            # be to construct N-dimensional arrays of pixel values for each
            # coordinate. However, if we are computing the coordinates for axis
            # i, and axis i is not dependent on any other axis, then the result
            # will be an N-dimensional array where the same 1D array of
            # coordinates will be repeated over and over.

            # To optimize this, we therefore essentially consider only the
            # dependent dimensions and then broacast the result to the full
            # array size at the very end.

            # view=None actually adds a dimension which is never what we really
            # mean, at least in glue.
            if view is None:
                view = Ellipsis

            # If the view is a tuple or list of arrays, we should actually just
            # convert these straight to world coordinates since the indices
            # of the pixel coordinates are the pixel coordinates themselves.
            if isinstance(view, (tuple, list)) and isinstance(view[0], np.ndarray):
                return np.array(self._data.coords.pixel2world(*view[::-1])[::-1])[self.axis]

            # For 1D arrays, slice can be given as a single slice but we need
            # to wrap it in a list to make the following code work correctly,
            # as it is then consistent with higher-dimensional cases.
            if isinstance(view, slice) or np.isscalar(view):
                view = [view]

            # Some views, e.g. with lists of integer arrays, can give arbitrarily
            # complex (copied) subsets of arrays, so in this case we don't do any
            # optimization
            if view is Ellipsis:
                optimize_view = False
            else:
                for v in view:
                    if not np.isscalar(v) and not isinstance(v, slice):
                        optimize_view = False
                        break
                else:
                    optimize_view = True

            pix_coords = []
            dep_coords = self._data.coords.dependent_axes(self.axis)

            final_slice = []
            final_shape = []

            for i in range(self._data.ndim):

                if optimize_view and i < len(view) and np.isscalar(view[i]):
                    final_slice.append(0)
                else:
                    final_slice.append(slice(None))

                # We set up a 1D pixel axis along that dimension.
                pix_coord = np.arange(self._data.shape[i])

                # If a view was specified, we need to take it into account for
                # that axis.
                if optimize_view and i < len(view):
                    pix_coord = pix_coord[view[i]]
                    if not np.isscalar(view[i]):
                        final_shape.append(len(pix_coord))
                else:
                    final_shape.append(self._data.shape[i])

                if i not in dep_coords:
                    # The axis is not dependent on this instance's axis, so we
                    # just compute the values once and broadcast along this
                    # dimension later.
                    pix_coord = 0

                pix_coords.append(pix_coord)

            # We build the list of N arrays, one for each pixel coordinate
            pix_coords = np.meshgrid(*pix_coords, indexing='ij', copy=False)

            # Finally we convert these to world coordinates
            axis = self._data.ndim - 1 - self.axis
            world_coords = self._data.coords.pixel2world_single_axis(*pix_coords[::-1],
                                                                     axis=axis)

            # We get rid of any dimension for which using the view should get
            # rid of that dimension.
            if optimize_view:
                world_coords = world_coords[tuple(final_slice)]

            # We then broadcast the final array back to what it should be
            world_coords = broadcast_to(world_coords, tuple(final_shape))

            # We apply the view if we weren't able to optimize before
            if optimize_view:
                return world_coords
            else:
                return world_coords[view]

        else:

            slices = [slice(0, s, 1) for s in self.shape]
            grids = np.broadcast_arrays(*np.ogrid[slices])
            if view is not None:
                grids = [g[view] for g in grids]
            return grids[self.axis]

    @property
    def shape(self):
        """ Tuple of array dimensions. """
        return self._data.shape

    @property
    def ndim(self):
        """ Number of dimensions """
        return len(self._data.shape)

    def __getitem__(self, key):
        return self._calculate(key)

    def __lt__(self, other):
        if self.world == other.world:
            return self.axis < other.axis
        return self.world

    def __gluestate__(self, context):
        return dict(axis=self.axis, world=self.world)

    @classmethod
    def __setgluestate__(cls, rec, context):
        return cls(None, rec['axis'], rec['world'])

    @property
    def numeric(self):
        return True

    @property
    def categorical(self):
        return False


class CategoricalComponent(Component):

    """
    Container for categorical data.
    """

    def __init__(self, categorical_data, categories=None, jitter=None, units=None):
        """
        :param categorical_data: The underlying :class:`numpy.ndarray`
        :param categories: List of unique values in the data
        :jitter: Strategy for jittering the data
        """

        super(CategoricalComponent, self).__init__(None, units)

        self._categorical_data = np.asarray(categorical_data)
        if self._categorical_data.ndim > 1:
            raise ValueError("Categorical Data must be 1-dimensional")

        self._categories = categories
        self._jitter_method = jitter
        self._is_jittered = False
        self._data = None
        if self._categories is None:
            self._update_categories()
        else:
            self._update_data()

    @property
    def codes(self):
        """
        The index of the category for each value in the array.
        """
        return self._data

    @property
    def labels(self):
        """
        The original categorical data.
        """
        return self._categorical_data

    @property
    def categories(self):
        """
        The categories.
        """
        return self._categories

    @property
    def data(self):
        warnings.warn("The 'data' attribute is deprecated. Use 'codes' "
                      "instead to access the underlying index of the "
                      "categories")
        return self.codes

    @property
    def numeric(self):
        return False

    @property
    def categorical(self):
        return True

    def _update_categories(self, categories=None):
        """
        :param categories: A sorted array of categories to find in the dataset.
        If None the categories are the unique items in the data.
        :return: None
        """
        if categories is None:
            categories, inv = unique(self._categorical_data)
            self._categories = categories
            self._data = inv.astype(np.float)
            self._data.setflags(write=False)
            self.jitter(method=self._jitter_method)
        else:
            if check_sorted(categories):
                self._categories = categories
                self._update_data()
            else:
                raise ValueError("Provided categories must be Sorted")

    def _update_data(self):
        """
        Converts the categorical data into the numeric representations given
        self._categories
        """
        self._is_jittered = False

        self._data = row_lookup(self._categorical_data, self._categories)
        self.jitter(method=self._jitter_method)
        self._data.setflags(write=False)

    def jitter(self, method=None):
        """
        Jitter the data so the density of points can be easily seen in a
        scatter plot.

        :param method: None | 'uniform':

        * None: No jittering is done (or any jittering is undone).
        * uniform: A unformly distributed random variable (-0.5, 0.5)
            is applied to each point.

        :return: None
        """

        if method not in set(['uniform', None]):
            raise ValueError('%s jitter not supported' % method)
        self._jitter_method = method
        seed = 1234567890
        rand_state = np.random.RandomState(seed)

        if (self._jitter_method is None) and self._is_jittered:
            self._update_data()
        elif (self._jitter_method is 'uniform') and not self._is_jittered:
            iswrite = self._data.flags['WRITEABLE']
            self._data.setflags(write=True)
            self._data += rand_state.uniform(-0.5, 0.5, size=self._data.shape)
            self._is_jittered = True
            self._data.setflags(write=iswrite)

    def subset_from_roi(self, att, roi, other_comp=None, other_att=None,
                        coord='x', is_nested=False):
        """
        Create a SubsetState object from an ROI.

        This encapsulates the logic for creating subset states with
        CategoricalComponents. There is an important caveat, only RangeROIs
        and RectangularROIs make sense in mixed type plots. As such, polygons
        are converted to their outer-most edges in this case.

        :param att: attribute name of this Component
        :param roi: an ROI object
        :param other_comp: The other Component for 2D ROIs
        :param other_att: The attribute name of the other Component
        :param coord: The orientation of this Component
        :param is_nested: True if this was passed from another Component.
        :return: A SubsetState (or subclass) object
        """

        if coord not in ('x', 'y'):
            raise ValueError('coord should be one of x/y')

        if isinstance(roi, RangeROI):

            # The selection is either an x range or a y range

            if roi.ori == coord:

                # The selection applies to the current component
                return CategoricalROISubsetState.from_range(self, att, roi.min, roi.max)

            else:

                # The selection applies to the other component, so we delegate
                other_coord = 'y' if coord == 'x' else 'x'
                return other_comp.subset_from_roi(other_att, roi,
                                                  other_comp=self,
                                                  other_att=att,
                                                  coord=other_coord)

        elif isinstance(roi, RectangularROI):

            # In this specific case, we can decompose the rectangular
            # ROI into two RangeROIs that are combined with an 'and'
            # logical operation.

            other_coord = 'y' if coord == 'x' else 'x'

            if coord == 'x':
                range1 = XRangeROI(roi.xmin, roi.xmax)
                range2 = YRangeROI(roi.ymin, roi.ymax)
            else:
                range2 = XRangeROI(roi.xmin, roi.xmax)
                range1 = YRangeROI(roi.ymin, roi.ymax)

            # We get the subset state for the current component
            subset1 = self.subset_from_roi(att, range1,
                                           other_comp=other_comp,
                                           other_att=other_att,
                                           coord=coord)

            # We now get the subset state for the other component
            subset2 = other_comp.subset_from_roi(other_att, range2,
                                                 other_comp=self,
                                                 other_att=att,
                                                 coord=other_coord)

            return AndState(subset1, subset2)

        elif isinstance(roi, CategoricalROI):

            # The selection is categorical itself

            return CategoricalROISubsetState(roi=roi, att=att)

        else:

            # The selection is polygon-like, which requires special care.

            if isinstance(other_comp, CategoricalComponent):

                # For each category, we check which categories along the other
                # axis fall inside the polygon:

                selection = {}

                for code, label in enumerate(self.categories):

                    # Determine the coordinates of the points to check
                    n_other = len(other_comp.categories)
                    y = np.arange(n_other)
                    x = np.repeat(code, n_other)

                    if coord == 'y':
                        x, y = y, x

                    # Determine which points are in the polygon, and which
                    # categories these correspond to
                    in_poly = roi.contains(x, y)
                    categories = other_comp.categories[in_poly]

                    if len(categories) > 0:
                        selection[label] = set(categories)

                return CategoricalROISubsetState2D(selection, att, other_att)

            else:

                # If the other component is not categorical, we treat this as if
                # each categorical component was mapped to a numerical value,
                # and at each value, we keep track of the polygon intersection
                # with the component. This will result in zero, one, or
                # multiple separate numerical ranges for each categorical value.

                # TODO: if we ever allow the category order to be changed, we
                # need to figure out how to update this!

                x, y = roi.to_polygon()

                if is_nested:
                    x, y = y, x

                # We loop over each category and for each one we find the
                # numerical ranges

                selection = {}

                for code, label in enumerate(self.categories):

                    # We determine all the numerical segments that represent the
                    # ensemble of points in y that fall in the polygon
                    # TODO: profile the following function
                    segments = polygon_line_intersections(x, y, xval=code)

                    if len(segments) > 0:
                        selection[label] = segments

                return CategoricalMultiRangeSubsetState(selection, att, other_att)

    def to_series(self, **kwargs):
        """ Convert into a pandas.Series object.

        This will be converted as a dtype=np.object!

        :param kwargs: All kwargs are passed to the Series constructor.
        :return: pandas.Series
        """

        return pd.Series(self._categorical_data.ravel(),
                         dtype=np.object, **kwargs)


class DateTimeComponent(Component):
    """
    A component representing a date/time.

    Parameters
    ----------
    data : `~numpy.ndarray`
        The data to store, with `~numpy.datetime64` dtype
    """

    def __init__(self, data, units=None):

        self.units = units

        if not isinstance(data, np.ndarray) or data.dtype.kind != 'M':
            raise TypeError("DateTimeComponent should be initialized with a datetim64 Numpy array")

        self._data = data

    @property
    def numeric(self):
        return True

    @property
    def datetime(self):
        return True
