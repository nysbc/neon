from typing import Any, Dict, Generator, List, Optional

import redminelib
from redminelib.resources.standard import Issue as RedmineIssue

from . import _fd, _u, o


class Connection:
    def __init__(self, url: str, key: str) -> None:
        self._url = url
        self._conn = redminelib.Redmine(url, key=key)

    def get(self, redmine_id: int) -> RedmineIssue:
        return self._conn.issue.get(redmine_id)

    def issues(
        self,
        project_id: str,
        updated_on: Optional[str] = None,
    ) -> Generator[RedmineIssue, None, None]:
        # yield self._conn.issue.get(19188)
        # return
        limit = 25
        kw: Dict[str, Any] = {
            "project_id": project_id,
            "limit": limit,
            "offset": 0,
        }
        if updated_on:
            kw["updated_on"] = ">=" + updated_on
        while True:
            issues: List[RedmineIssue] = self._conn.issue.filter(**kw)
            if not issues:
                break
            yield from issues
            kw["offset"] += limit

    def emgusers(self, **kw: Any) -> Generator[o.EmgUser, None, None]:
        for issue in self.issues(_u.project.EmgUsers, **kw):
            yield o.EmgUser(issue, self._url)

    def emgprojects(self, **kw: Any) -> Generator[o.EmgProject, None, None]:
        for issue in self.issues(_u.project.EmgProjects, **kw):
            yield o.EmgProject(issue, self._url)

    # Redmine Bug?  If a request for a cf (custom field) is made to a field
    # that's not flagged as "filter" and "searchable" redmine seems to return
    # all issues in the project the issue belongs to.  This is bad bad bad!
    # To prevent modifying redmine issues that do not conform to the request,
    # assert the attribute in the object returned = the requested value.

    def _emgusers_for_cf(
        self, field: _fd.cf, value: str, status: str = "open"
    ) -> List[o.EmgUser]:
        issues: List[RedmineIssue] = self._conn.issue.filter(
            project_id=_u.project.EmgUsers,
            status_id=status,
            **{field.value.search_id: value},
        )
        if not issues:
            return []
        users = list(map(lambda issue: o.EmgUser(issue, self._url), issues))
        assert field.value.attr
        for user in users:
            if getattr(user, field.value.attr) != value:
                raise Exception(
                    f"{user}\n {getattr(user, field.value.attr)} != {value}"
                )
        return users

    def _emgprojects_for_cf(
        self, field: _fd.cf, value: str
    ) -> List[o.EmgProject]:
        issues: List[RedmineIssue] = self._conn.issue.filter(
            project_id=_u.project.EmgProjects,
            **{field.value.search_id: value},
        )
        if not issues:
            return []
        projects = list(
            map(lambda issue: o.EmgProject(issue, self._url), issues)
        )
        assert field.value.attr
        for p in projects:
            if getattr(p, field.value.attr) != value:
                raise Exception(
                    f"{p}\n {getattr(p, field.value.attr)} != {value}"
                )
        return projects

    def emguser_for_ldap(
        self, ldap: str, status: str = "open"
    ) -> Optional[o.EmgUser]:
        users = self._emgusers_for_cf(_fd.cf.LDAP_UserName, ldap, status)
        if not users:
            return None
        assert len(users) == 1
        return users[0]

    def emguser_for_email(self, email: str) -> Optional[o.EmgUser]:
        users = self._emgusers_for_cf(_fd.cf.PrimaryUserEmail, email)
        if not users:
            return None
        assert len(users) == 1
        return users[0]

    def emgusers_for_email(self, email: str) -> List[o.EmgUser]:
        "for debugging - (primary) user emails are unique"
        users = self._emgusers_for_cf(_fd.cf.PrimaryUserEmail, email)
        if not users:
            return []
        return users

    def emgusers_for_pi_email(self, email: str) -> List[o.EmgUser]:
        return self._emgusers_for_cf(_fd.cf.PI_Email, email)

    def emgusers_for_ppms_group(self, group: str) -> List[o.EmgUser]:
        return self._emgusers_for_cf(_fd.cf.PPMS_Group, group)

    def emgprojects_for_email(self, email: str) -> List[o.EmgProject]:
        return self._emgprojects_for_cf(_fd.cf.PrimaryUserEmail, email)

    def emgprojects_for_pi_email(self, email: str) -> List[o.EmgProject]:
        return self._emgprojects_for_cf(_fd.cf.PI_Email, email)

    def emgprojects_for_pppms_group(self, group: str) -> List[o.EmgProject]:
        return self._emgprojects_for_cf(_fd.cf.PPMS_Group, group)

    # pylint: disable=protected-access
    def update(self, *args: o.Base) -> None:
        for a in args:
            _, cf = a._pending()
            if not cf:
                continue
            self._conn.issue.update(a.id(), custom_fields=cf)
            a._commit()

    def close(self, *args: o.Base) -> None:
        for a in args:
            self._conn.issue.update(a.id(), status_id=5)


class LazyConnection:
    def __init__(self, url: str, key: str) -> None:
        self._url = url
        self._key = key
        self._conn: Optional[Connection] = None

    def __call__(self) -> Connection:
        if self._conn:
            return self._conn
        self._conn = Connection(self._url, self._key)
        return self._conn


__all__ = ["Connection", "LazyConnection"]
