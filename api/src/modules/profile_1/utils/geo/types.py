from typing import List, Optional, Tuple, Union

BBox = Union[
    Tuple[float, float, float, float],  # 2D bbox
    Tuple[float, float, float, float, float, float],  # 3D bbox
]


def validate_bbox(bbox: Optional[BBox]) -> Optional[BBox]:
    """Validate BBox values are ordered correctly."""
    # If bbox is None, there is nothing to validate.
    if bbox is None:
        return None

    # A list to store any errors found so we can raise them all at once.
    errors: List[str] = []

    # Determine where the second position starts. 2 for 2D, 3 for 3D.
    offset = len(bbox) // 2

    # Check X
    if bbox[0] > bbox[offset]:
        errors.append(f"Min X ({bbox[0]}) must be <= Max X ({bbox[offset]}).")
    # Check Y
    if bbox[1] > bbox[1 + offset]:
        errors.append(f"Min Y ({bbox[1]}) must be <= Max Y ({bbox[1 + offset]}).")
    # If 3D, check Z values.
    if offset > 2 and bbox[2] > bbox[2 + offset]:
        errors.append(f"Min Z ({bbox[2]}) must be <= Max Z ({bbox[2 + offset]}).")

    # Raise any errors found.
    if errors:
        raise ValueError("Invalid BBox. Error(s): " + " ".join(errors))

    return bbox


Position = Union[Tuple[float, float], Tuple[float, float, float]]
