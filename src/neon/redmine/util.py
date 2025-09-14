from typing import Optional

from redminelib.resources.standard import Issue as RedmineIssue


def custom(issue: RedmineIssue, name: str) -> Optional[str]:
    """returns None if the custom_field is not defined;
    otherwise returns stripped() string"""
    if not hasattr(issue, "custom_fields"):
        return None
    customfields = issue.custom_fields.values()  # pyright: ignore
    for field in customfields:
        if field["name"] == name:
            v = field["value"]
            # custom fields values can be None
            if not v:
                return ""
            assert isinstance(v, str)
            return v.strip()
    return None


def mustcustom(issue: RedmineIssue, name: str) -> str:
    if (v := custom(issue, name)) is None:
        raise Exception(
            f"issue [{issue.id}] does not define custom field [{name}]"
        )
    return v


def prcustom(issue: RedmineIssue) -> None:
    customfields = issue.custom_fields.values()  # pyright: ignore
    for field in customfields:
        print(f"{field['name']} :: {field['value']}")
