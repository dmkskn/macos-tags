"""A python libraty for working with macOS tags"""
from __future__ import annotations

import plistlib
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, List, Optional, Sequence, Union

import mdfind  # type: ignore
import xattr  # type: ignore

_XATTR_TAGS = "com.apple.metadata:_kMDItemUserTags"
_XATTR_FINDER_INFO = "com.apple.FinderInfo"


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


def _get_tag_name(tag: Union[str, Tag]) -> str:
    return tag.splitlines()[0] if isinstance(tag, str) else tag.name


def _get_raw_tags(file: str) -> List[str]:
    # Like ["tag-one\n4", "tag-two\n6", tag-three"]
    plist = xattr.getxattr(file, _XATTR_TAGS)
    return plistlib.loads(plist)


def _remove_finder_info(file: str) -> None:
    # If you don't delete the com.apple.FinderInfo extended attributes,
    # Finder keeps showing the color labels for tags with colors.
    if _XATTR_FINDER_INFO in xattr.listxattr(file):
        xattr.removexattr(file, _XATTR_FINDER_INFO)


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
    return [Tag.from_string(tag) for tag in _get_raw_tags(file)]


def set_all(tags: Sequence[Union[str, Tag]], *, file: str) -> None:
    """Add `tags` to the `file` and remove the rest."""
    _remove_finder_info(file)
    plist = plistlib.dumps([str(tag) for tag in tags])  # type: ignore
    xattr.setxattr(file, _XATTR_TAGS, plist)


def remove_all(file: str) -> None:
    """Remove all tags from the `file`."""
    set_all([], file=file)


def add(tag: Union[str, Tag], *, file: str) -> None:
    """Add `tag` to `file`."""
    tag = Tag.from_string(tag) if isinstance(tag, str) else tag
    tags = get_all(file)
    if tag not in tags:
        tags.append(tag)
        set_all(tags, file=file)


def remove(tag: Union[str, Tag], *, file: str) -> None:
    """Remove `tag` from `file`."""
    tag = Tag.from_string(tag) if isinstance(tag, str) else tag
    tags = get_all(file)
    if tag in tags:
        tags.pop(tags.index(tag))
        set_all(tags, file=file)
