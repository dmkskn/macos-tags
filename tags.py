"""A python libraty for working with macOS tags"""
from typing import List, NamedTuple, Optional, Union

import mdfind  # type: ignore

_MDFIND_TAGS_QUERY = "kMDItemUserTags=={tag_name}"


class Tag(NamedTuple):
    """A named tuple that represents a single tag.

    Usage: `Tag(name="tag-name", color=tags.BLUE)`.
    """

    name: str
    color: Optional[int] = None


def _get_tag_name(tag: Union[str, Tag]) -> str:
    return tag.splitlines()[0] if isinstance(tag, str) else tag.name


def find(tag: Union[str, Tag], *, onlyin: Optional[str] = None) -> List[str]:
    """Find files by `tag`."""
    tag_name = _get_tag_name(tag)
    return mdfind.query(query=f"kMDItemUserTags=={tag_name}", onlyin=onlyin)


def count(tag: Union[str, Tag], *, onlyin: Optional[str] = None) -> int:
    """Output the total number of files by `tag`."""
    tag_name = _get_tag_name(tag)
    return mdfind.count(query=f"kMDItemUserTags=={tag_name}", onlyin=onlyin)
