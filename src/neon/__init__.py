import os
from typing import Any, Dict, cast

from . import ppms, redmine


def config(section: str) -> Dict[str, Any]:
    with open(os.environ["NEON_CONFIG"]) as config:
        ns: Dict[str, Any] = {}
        exec(config.read(), ns)
        return cast(Dict[str, Any], ns[section])
