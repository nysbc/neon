from enum import Enum, unique
from typing import Final, Optional

# field descriptor for custom fields


class _cf:
    def __init__(self, uid: int, desc: str, attr: Optional[str] = None) -> None:
        self.id: Final = uid
        self.name: Final = desc
        self.attr: Final = attr

    @property
    def search_id(self) -> str:
        return f"cf_{self.id}"

    def __hash__(self) -> int:
        return hash((self.id, self.name))

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, _cf)
        return (self.id, self.name) == (
            other.id,
            other.name,
        )


# if a cf is used in conn requests it must define an attr. see note in conn.py.


@unique
class cf(Enum):
    FirstName = _cf(42, "First Name")
    LabeledGridBoxes = _cf(133, "Labeled Grid Boxes")
    LastName = _cf(43, "Last Name")
    NC_City = _cf(81, "NC-City")
    NC_LabMailingAddress = _cf(129, "NC-Lab Mailing Address")
    NC_ProjectId = _cf(74, "NC-Project ID")
    NC_State = _cf(82, "NC-State")
    NC_Zip = _cf(128, "NC-Zip")
    PI = _cf(135, "PI")
    PI_Email = _cf(25, "PI email", attr="pi_email")
    PPMS_Group = _cf(63, "PPMS Group Identifier", attr="ppms_group")
    PrimaryUserEmail = _cf(27, "Primary User Email", attr="email")
