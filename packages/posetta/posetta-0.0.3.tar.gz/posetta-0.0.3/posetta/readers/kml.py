"""XML style format

Description:
------------


Example:
--------



Specification:
--------------

http://www.opengeospatial.org/standards/kml/

"""

from fastkml import kml
import numpy as np
import pandas as pd

# Posetta imports
from posetta import data
from posetta.lib import plugins
from posetta.readers._reader import Reader


@plugins.register
class KmlReader(Reader):
    """A reader for KML-files
    """
    def setup_reader(self) -> None:
        """Set up a reader so that it can read data from a file."""
        self.kml = kml.KML()

    def read_data(self) -> None:
        """Read data from the data file

        Data should be read from `self.input_stream` and stored in the
        dictionary `self.data`. A description of the data may be placed
        in the dictionary `self.meta`.
        """
        try:
            bytes(self.input_stream)
        except TypeError:
            pass  # Figure out how to fix this bug: from_string crashes without the previous line
        kml_string = self.input_stream.read()
        self.kml.from_string(kml_string)
        for point, description in self._points(self.kml.features()):
            self.data.setdefault("__points__", list()).append(np.array(point))
            for k, v in description.items():
                self.data.setdefault(k, list()).append(v)

    def _points(self, features):
        """Find points and description recursively"""
        for feature in features:
            if hasattr(feature, "geometry"):
                if feature.description is None:
                    continue
                points = feature.geometry
                description = pd.read_html(feature.description)[0]
                description = description.set_index(description[0]).drop(columns=0)
                description = description.to_dict()[1]
                yield points, description
            else:
                yield from self._points(feature.features())

    def as_coordset(self) -> data.CoordSet:
        """Return the data as a coordinate dataset

        Returns:
            The data that has been read as a coordinate dataset.
        """
        cset = data.CoordSet()
        points = np.array(self.data.pop("__points__"))
        num_points = len(points)
        for idx, value in enumerate(points.T):
            cset.add("positions", val=value, idx=idx, column_name="xyz"[idx])

        for column, value in self.data.items():
            if value.ndim == 0 or len(value) != num_points:
                continue
            cset.add("values", val=value, column_name=column)

        return cset
