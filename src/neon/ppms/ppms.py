from typing import Dict, List, Optional, cast

import pyppms
import pyppms.user


class Group:
    def __init__(self, data: Dict[str, str]) -> None:
        self._data = data

    @property
    def name(self) -> str:
        return self._data["unitlogin"]

    @property
    def pi_first(self) -> Optional[str]:
        name = self._data["headname"].split(",")
        if len(name) == 1:
            return None
        return name[1].strip()

    @property
    def pi_last(self) -> str:
        name = self._data["headname"].split(",")
        return name[0].strip()

    @property
    def pi_email(self) -> str:
        return self._data["heademail"].strip().lower()

    @property
    def active(self) -> bool:
        return bool(self._data["active"])

    def __str__(self) -> str:
        return f"[{self.name}|{self.pi_email}]"


class Connection:
    def __init__(self, url: str, key: str) -> None:
        self._conn = pyppms.PpmsConnection(url, key)

    def maybe_group(self, gid: str) -> Optional[Group]:
        try:
            return Group(self._conn.get_group(gid))
        except KeyError:
            return None

    def group(self, gid: str) -> Group:
        if (g := self.maybe_group(gid)) is None:
            raise Exception()
        return g

    def groups(self) -> List[str]:
        return cast(List[str], self._conn.get_groups())

    def users_for_group(self, gid: str) -> List[pyppms.user.PpmsUser]:
        return cast(List[pyppms.user.PpmsUser], self._conn.get_group_users(gid))


__all__ = ["Group", "Connection"]
