"""A python libraty for working with macOS tags"""
import plistlib
from typing import Any, List, NamedTuple, Optional, Union

import mdfind  # type: ignore
import xattr  # type: ignore

_XATTR_TAGS = "com.apple.metadata:_kMDItemUserTags"


class Tag(NamedTuple):
    """A named tuple that represents a single tag.

    Usage: `Tag(name="tag-name", color=tags.BLUE)`.
    """

    name: str
    color: Optional[int] = None


def _get_tag_name(tag: Union[str, Tag]) -> str:
    return tag.splitlines()[0] if isinstance(tag, str) else tag.name


def _get_raw_tags(file: str) -> List[str]:
    plist = xattr.getxattr(file, _XATTR_TAGS)
    return plistlib.loads(plist)


def find(tag: Union[str, Tag], *, onlyin: Optional[str] = None) -> List[str]:
    """Find files by `tag`."""
    tag_name = _get_tag_name(tag)
    return mdfind.query(query=f"kMDItemUserTags=={tag_name}", onlyin=onlyin)


def count(tag: Union[str, Tag], *, onlyin: Optional[str] = None) -> int:
    """Output the total number of files by `tag`."""
    tag_name = _get_tag_name(tag)
    return mdfind.count(query=f"kMDItemUserTags=={tag_name}", onlyin=onlyin)


def get_all(file: str) -> List[Tag]:
    """List the tags on the `file`."""
    tags: List[Tag] = []
    for tag in _get_raw_tags(file):
        if "\n" in tag:
            tag_name, tag_color = tag.splitlines()
            tags.append(Tag(name=tag_name, color=int(tag_color)))
        else:
            tags.append(Tag(name=tag, color=None))

    return tags
