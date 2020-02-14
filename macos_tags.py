"""A python libraty for working with macOS tags"""
from __future__ import annotations

import plistlib
import sys
from dataclasses import dataclass, field
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

import mdfind  # type: ignore
import xattr  # type: ignore


def _test_os() -> None:
    """Raise an error if it's not MacOS."""
    if sys.platform != "darwin":
        raise RuntimeError(f"The library works only on macOS.")


_test_os()


__all__ = [
    "Color",
    "Tag",
    "find",
    "count",
    "get_all",
    "set_all",
    "remove_all",
    "add",
    "remove",
]


_XATTR_TAGS = "com.apple.metadata:_kMDItemUserTags"
_XATTR_FINDER_INFO = "com.apple.FinderInfo"
_MDFIND_TAGS_QUERY = "kMDItemUserTags=={}"
_ALL_TAGS_PLIST_PATH = f"{Path.home()}/Library/SyncedPreferences/com.apple.finder.plist"


@unique
class Color(Enum):
    GRAY = 1
    GREEN = 2
    PURPLE = 3
    BLUE = 4
    YELLOW = 5
    RED = 6
    ORANGE = 7

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Tag:
    """Represents a single tag."""

    name: str
    color: Optional[Color] = field(default=None, compare=False)

    def __str__(self) -> str:
        if self.color:
            return f"{self.name}\n{self.color}"
        return self.name

    @classmethod
    def from_string(self, tag: str) -> Tag:
        """Create tag from string (like `"tag"` or `"tag\\n1"`)"""
        if "\n" in tag:
            name, color = tag.splitlines()
            return Tag(name, Color(int(color)))
        else:
            return Tag(tag)


AnyTag = Union[str, Tag]


def _create_tag(tag: AnyTag) -> Tag:
    return Tag.from_string(tag) if isinstance(tag, str) else tag


def _get_raw_tags(file: str) -> List[str]:
    # Like ["tag-one\n4", "tag-two\n6", tag-three"]
    try:
        plist = xattr.getxattr(file, _XATTR_TAGS)
    except OSError:
        # There is no _XATTR_TAGS attribute
        return []
    return plistlib.loads(plist)


def _remove_finder_info(file: str) -> None:
    # If you don't delete the com.apple.FinderInfo extended attributes,
    # Finder keeps showing the color labels for tags with colors.
    if _XATTR_FINDER_INFO in xattr.listxattr(file):
        xattr.removexattr(file, _XATTR_FINDER_INFO)


def find(tag: AnyTag, *, onlyin: Optional[str] = None) -> List[str]:
    """Find files by `tag`."""
    tag = _create_tag(tag)
    return mdfind.query(query=_MDFIND_TAGS_QUERY.format(tag.name), onlyin=onlyin)


def count(tag: AnyTag, *, onlyin: Optional[str] = None) -> int:
    """Output the total number of files by `tag`."""
    tag = _create_tag(tag)
    return mdfind.count(query=_MDFIND_TAGS_QUERY.format(tag.name), onlyin=onlyin)


def get_all(file: str) -> List[Tag]:
    """List the tags on the `file`."""
    return [Tag.from_string(tag) for tag in _get_raw_tags(file)]


def set_all(tags: Sequence[AnyTag], *, file: str) -> None:
    """Add `tags` to the `file` and remove the rest."""
    _remove_finder_info(file)
    plist = plistlib.dumps([str(tag) for tag in tags])  # type: ignore
    xattr.setxattr(file, _XATTR_TAGS, plist)


def remove_all(file: str) -> None:
    """Remove all tags from the `file`."""
    set_all([], file=file)


def add(tag: AnyTag, *, file: str) -> None:
    """Add `tag` to `file`."""
    tag = _create_tag(tag)
    tags = get_all(file)
    if tag not in tags:
        tags.append(tag)
        set_all(tags, file=file)


def remove(tag: AnyTag, *, file: str) -> None:
    """Remove `tag` from `file`."""
    tag = _create_tag(tag)
    tags = get_all(file)
    if tag in tags:
        tags.pop(tags.index(tag))
        set_all(tags, file=file)


def tags() -> List[Tag]:
    """Get all tags."""
    with open(_ALL_TAGS_PLIST_PATH, "rb") as fp:
        data: Dict["str", Any] = plistlib.load(fp)
        result = []
        for tag in data["values"]["FinderTagDict"]["value"]["FinderTags"]:
            color = None if tag.get("l") is None else Color(tag["l"])
            result.append(Tag(tag["n"], color))
        return result
