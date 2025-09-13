import datetime
from typing import Dict, Final, List, Tuple

from redminelib.resources.standard import Issue as RedmineIssue

from .. import u
from . import fd, util


class Base:
    class _Field:
        def __init__(self, name: str, value: str) -> None:
            self._dirty = False
            self.name: Final = name
            self._value = value

        @property
        def value(self) -> str:
            return self._value

        @value.setter
        def value(self, v: str) -> None:
            if self._value == v:
                return
            self._value = v
            self._dirty = True

        def isdirty(self) -> bool:
            return self._dirty is True

        def clean(self) -> None:
            self._dirty = False

    def __init__(self, issue: RedmineIssue) -> None:
        self._issue = issue
        self._custom_fields: Dict[fd.cf, Base._Field] = {}

    def id(self) -> int:
        x: Final = self._issue.id
        assert isinstance(x, int)
        return x

    def __hash__(self) -> int:
        return self.id()

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, EmgUser)
        return self.id() == other.id()

    def _commit(self) -> None:
        for f in self._custom_fields.values():
            f.clean()

    def _custom(self, field: fd.cf) -> _Field:
        if not field in self._custom_fields:
            self._custom_fields[field] = Base._Field(
                name=field.value.name,
                value=util.mustcustom(self._issue, field.value.name),
            )
        return self._custom_fields[field]

    def _pending(self) -> Tuple[Dict[str, str], List[Dict[str, int | str]]]:
        std: Dict[str, str] = {}  # fixme impl - is it needed?
        cf: List[Dict[str, int | str]] = []
        for k, v in self._custom_fields.items():
            if v.isdirty():
                cf.append({"id": k.value.id, "value": v.value})
        return std, cf

    @property
    def email(self) -> str:
        return self._custom(fd.cf.PrimaryUserEmail).value

    @email.setter
    def email(self, value: str) -> None:
        self._custom(fd.cf.PrimaryUserEmail).value = value

    @property
    def pi_email(self) -> str:
        return self._custom(fd.cf.PI_Email).value

    @pi_email.setter
    def pi_email(self, value: str) -> None:
        self._custom(fd.cf.PI_Email).value = value

    @property
    def url(self) -> str:
        return f"{u.redmine.url}/issues/{self._issue.id}"

    def __str__(self) -> str:
        return f"{self._issue} ({self.url})"


class EmgUser(Base):
    def ispi(self) -> bool:
        return self.email == self.pi_email

    @property
    def pi(self) -> str:
        return self._custom(fd.cf.PI).value

    @pi.setter
    def pi(self, value: str) -> None:
        self._custom(fd.cf.PI).value = value

    @property
    def ppms_group(self) -> str:
        return self._custom(fd.cf.PPMS_Group).value

    @property
    def firstname(self) -> str:
        return self._custom(fd.cf.FirstName).value

    @property
    def lastname(self) -> str:
        return self._custom(fd.cf.LastName).value

    @property
    def name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    @property
    def labeled_grid_boxes(self) -> str:
        return self._custom(fd.cf.LabeledGridBoxes).value

    @labeled_grid_boxes.setter
    def labeled_grid_boxes(self, value: str) -> None:
        self._custom(fd.cf.LabeledGridBoxes).value = value

    @property
    def ldap(self) -> str:
        return util.mustcustom(self._issue, "LDAP Username")

    def __str__(self) -> str:
        return f"{self.name} ({self.url})"


class EmgProject(Base):
    @property
    def ppms_group(self) -> str:
        return util.mustcustom(self._issue, "PPMS Group Identifier")

    @property
    def primary_user_name(self) -> str:
        return util.mustcustom(self._issue, "Primary User Name")

    @property
    def start_date(self) -> datetime.date:
        x = self._issue.start_date
        assert isinstance(x, datetime.date)
        return x

    @property
    def institution(self) -> str:
        return util.mustcustom(self._issue, "Institution")

    @property
    def nc_project_id(self) -> str:
        return self._custom(fd.cf.NC_ProjectId).value

    @nc_project_id.setter
    def nc_project_id(self, value: str) -> None:
        self._custom(fd.cf.NC_ProjectId).value = value

    def __str__(self) -> str:
        return f"{self._issue} ({self.url})"


class Proposal_v2(Base):
    def nc_project_id(self) -> str:
        return util.mustcustom(self._issue, "NC-Project ID")

    @property
    def labmailingaddress(self) -> str:
        return self._custom(fd.cf.NC_LabMailingAddress).value

    @labmailingaddress.setter
    def labmailingaddress(self, value: str) -> None:
        self._custom(fd.cf.NC_LabMailingAddress).value = value

    @property
    def city(self) -> str:
        return self._custom(fd.cf.NC_City).value

    @city.setter
    def city(self, value: str) -> None:
        self._custom(fd.cf.NC_City).value = value

    @property
    def state(self) -> str:
        return self._custom(fd.cf.NC_State).value

    @state.setter
    def state(self, value: str) -> None:
        self._custom(fd.cf.NC_State).value = value

    @property
    def zip(self) -> str:
        return self._custom(fd.cf.NC_Zip).value

    @zip.setter
    def zip(self, value: str) -> None:
        self._custom(fd.cf.NC_Zip).value = value
