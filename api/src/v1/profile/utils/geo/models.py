from pydantic import field_validator, BaseModel
from typing import Any, Optional, Literal
import abc

from src.v1.base.schemas import BaseSchema
from .types import BBox, validate_bbox, Position
from .mixins import GeoInterfaceMixin


def _position_wkt_coordinates(coordinates: Position, force_z: bool = False) -> str:
    """Converts a Position to WKT Coordinates."""
    wkt_coordinates = " ".join(str(number) for number in coordinates)
    if force_z and len(coordinates) < 3:
        wkt_coordinates += " 0.0"
    return wkt_coordinates


def _position_has_z(position: Position) -> bool:
    return len(position) == 3


class _GeometryBase(BaseSchema, abc.ABC, GeoInterfaceMixin):
    """Base class for geometry models"""

    type: str
    coordinates: Any
    bbox: Optional[BBox] = None

    @abc.abstractmethod
    def __wkt_coordinates__(self, coordinates: Any, force_z: bool) -> str:
        """return WKT coordinates."""
        ...

    @property
    @abc.abstractmethod
    def has_z(self) -> bool:
        """Checks if any coordinate has a Z value."""
        ...

    @property
    def wkt(self) -> str:
        """Return the Well Known Text representation."""
        # Start with the WKT Type
        wkt = self.type.upper()
        has_z = self.has_z
        if self.coordinates:
            # If any of the coordinates have a Z add a "Z" to the WKT
            wkt += " Z " if has_z else " "
            # Add the rest of the WKT inside parentheses
            wkt += f"({self.__wkt_coordinates__(self.coordinates, force_z=has_z)})"
        else:
            # Otherwise it will be "EMPTY"
            wkt += " EMPTY"

        return wkt

    _validate_bbox = field_validator("bbox")(validate_bbox)


class Point(_GeometryBase):
    """Point Model"""

    type: Literal["Point"] = "Point"
    coordinates: Position

    def __wkt_coordinates__(self, coordinates: Any, force_z: bool) -> str:
        """return WKT coordinates."""
        return _position_wkt_coordinates(coordinates, force_z)

    @property
    def has_z(self) -> bool:
        """Checks if any coordinate has a Z value."""
        return _position_has_z(self.coordinates)
