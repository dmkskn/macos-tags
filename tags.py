"""A python libraty for working with macOS tags"""
from __future__ import annotations

import plistlib
from typing import Any, List, NamedTuple, Optional, Sequence, Union

import mdfind  # type: ignore
import xattr  # type: ignore

_XATTR_TAGS = "com.apple.metadata:_kMDItemUserTags"
_XATTR_FINDER_INFO = "com.apple.FinderInfo"


class Tag(NamedTuple):
    """A named tuple that represents a single tag.

    Usage: `Tag(name="tag-name", color=tags.BLUE)`.
    """

    name: str
    color: Optional[int] = None

    def __str__(self) -> str:
        if self.color:
            return f"{self.name}\n{self.color}"
        return self.name

    @classmethod
    def create(self, tag: str) -> Tag:
        """Create tag from string (like `"tag"` or `"tag\\n1"`)"""
        if "\n" in tag:
            name, color = tag.splitlines()
            return Tag(name, int(color))
        else:
            return Tag(tag)


def _get_tag_name(tag: Union[str, Tag]) -> str:
    return tag.splitlines()[0] if isinstance(tag, str) else tag.name


def _get_raw_tags(file: str) -> List[str]:
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
    return [Tag.create(tag) for tag in _get_raw_tags(file)]


def set_all(tags: Sequence[Union[str, Tag]], *, file: str) -> None:
    """Add `tags` to the `file` and remove the rest."""
    _remove_finder_info(file)
    plist = plistlib.dumps([str(tag) for tag in tags])  # type: ignore
    xattr.setxattr(file, _XATTR_TAGS, plist)


def remove_all(file: str) -> None:
    """Remove all tags from the `file`"""
    set_all([], file=file)
