from textwrap import wrap
from typing import Any, Dict


def genSubtitleFromFilters(filters: Dict[str, Any]) -> str:
    # Create a subtitle based on the filters applied
    subtitle: str = "\n".join(
        wrap(
            (
                "Filters applied: "
                + ", ".join(
                    [f"{key}={value}" for key, value in (filters or {}).items()]
                )
                if filters
                else "No filters applied"
            ),
            width=80,
        )
    )
    return subtitle
