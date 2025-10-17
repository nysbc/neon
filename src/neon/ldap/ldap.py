import abc
from typing import Any, Dict, Generator, Optional

import ldap3
import ldap3.abstract.entry
import ldap3.utils.conv


class User(abc.ABC):
    attributes = ["uid", "mail", "gidNumber"]

    @property
    @abc.abstractmethod
    def username(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def email(self) -> Optional[str]:
        pass

    def __str__(self) -> str:
        return "%s: %s" % (self.username, self.email)


class DataUser(User):
    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data
        self._attributes = data["attributes"]

    @property
    def username(self) -> str:
        xs = self._attributes["uid"]
        assert len(xs) == 1
        x = xs[0]
        assert isinstance(x, str)
        return x

    @property
    def email(self) -> Optional[str]:
        xs = self._attributes["mail"]
        if len(xs) == 0:
            return None
        assert len(xs) == 1
        x = xs[0]
        assert isinstance(x, str)
        return x


class EntryUser(User):
    def __init__(self, entry: ldap3.abstract.entry.Entry) -> None:
        self._entry = entry

    @property
    def username(self) -> str:
        x = self._entry.uid.value
        assert isinstance(x, str)
        return x

    @property
    def email(self) -> Optional[str]:
        x = self._entry.mail.value
        assert isinstance(x, str)
        return x


class Connection:
    def __init__(self, spec: Dict[str, str]) -> None:
        self._conn = ldap3.Connection(
            spec["LDAP_URI"],
            spec["LDAP_BIND_DN"],
            spec["LDAP_PASSWORD"],
            auto_bind=True,
        )
        self._spec = spec

    def users(self) -> Generator[User, None, None]:
        entries = self._conn.extend.standard.paged_search(
            self._spec["LDAP_USERS_OU"],
            "(objectClass=posixAccount)",
            attributes=User.attributes,
            paged_size=1000,
        )
        for e in entries:
            yield DataUser(e)

    def user_for_uid(self, uid: str) -> Optional[User]:
        uid = ldap3.utils.conv.escape_filter_chars(uid)
        user = self._conn.search(
            self._spec["LDAP_USERS_OU"],
            f"(&(objectClass=posixAccount)(uid={uid}))",
            attributes=User.attributes,
        )
        if not user:
            return None
        assert len(self._conn.entries) == 1
        return EntryUser(self._conn.entries[0])


__all__ = ["Connection"]
