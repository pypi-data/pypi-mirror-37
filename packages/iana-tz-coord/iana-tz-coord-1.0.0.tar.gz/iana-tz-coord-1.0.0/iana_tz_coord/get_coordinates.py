from iana_tz_coord import Coordinates
from iana_tz_coord.coordinates_by_tz_name import COORDINATES_BY_TZ_NAME


def get_coordinates(tz_name: str) -> Coordinates:
    try:
        return COORDINATES_BY_TZ_NAME[tz_name]
    except LookupError:
        raise LookupError(f'Could not find coordinates for "{tz_name}"')
