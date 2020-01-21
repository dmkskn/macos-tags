from unittest.mock import call, patch

import tags

RAW_PLIST = b"bplist00\xa2\x01\x02Ttag1Vtag2\n5\x08\x0b\x10\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17"
CLEAN_PLIST = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<array>\n\t<string>tag1</string>\n\t<string>tag2\n5</string>\n</array>\n</plist>\n'
RAW_TAGS = ["tag1", "tag2\n5"]  # from plist
CLEAN_TAGS = [tags.Tag(name="tag1", color=None), tags.Tag(name="tag2", color=5)]


def test_create_tag_object_from_string():
    assert tags.Tag.create("tag1") == tags.Tag("tag1", None)
    assert tags.Tag.create("tag1\n1") == tags.Tag("tag1", 1)


def test_str_in_tag_object():
    assert str(tags.Tag("tag1", None)) == "tag1"
    assert str(tags.Tag("tag1", 1)) == "tag1\n1"


def test_get_tag_name_from_tag_object():
    assert tags._get_tag_name(tags.Tag("tag1")) == "tag1"


def test_get_tag_name_from_string():
    assert tags._get_tag_name("tag1") == "tag1"


def test_get_tag_name_from_string_with_color_mark():
    assert tags._get_tag_name("tag1\n1") == "tag1"


@patch("mdfind.query")
def test_find_works_with_string(query):
    _ = tags.find("tag1", onlyin="/path")
    assert query.called
    assert query.call_args == call(query="kMDItemUserTags==tag1", onlyin="/path")


@patch("mdfind.query")
def test_find_works_with_tag_object(query):
    _ = tags.find(tags.Tag("tag1"), onlyin="/path")
    assert query.called
    assert query.call_args == call(query="kMDItemUserTags==tag1", onlyin="/path")


@patch("mdfind.query")
def test_find_works_with_string_with_color_mark(query):
    _ = tags.find("tag1\n1", onlyin="/path")
    assert query.called
    assert query.call_args == call(query="kMDItemUserTags==tag1", onlyin="/path")


@patch("mdfind.count")
def test_counts_works_with_string(count):
    _ = tags.count("tag1", onlyin="/path")
    assert count.called
    assert count.call_args == call(query="kMDItemUserTags==tag1", onlyin="/path")


@patch("mdfind.count")
def test_count_works_with_tag_object(count):
    _ = tags.count(tags.Tag("tag1"), onlyin="/path")
    assert count.called
    assert count.call_args == call(query="kMDItemUserTags==tag1", onlyin="/path")


@patch("mdfind.count")
def test_count_works_with_string_with_color_mark(count):
    _ = tags.count("tag1\n1", onlyin="/path")
    assert count.called
    assert count.call_args == call(query="kMDItemUserTags==tag1", onlyin="/path")


@patch("xattr.getxattr", return_value=RAW_PLIST)
def test_get_raw_tags(getxattr):
    result = tags._get_raw_tags("/path")
    assert getxattr.called
    assert result == RAW_TAGS


@patch("tags._get_raw_tags", return_value=RAW_TAGS)
def test_get_all(_get_raw_tags):
    result = tags.get_all("/path")
    assert _get_raw_tags.called
    assert result == CLEAN_TAGS


@patch("xattr.removexattr")
@patch("xattr.listxattr", return_value=["com.apple.FinderInfo"])
def test_remove_finder_info(listxattr, removexattr):
    tags._remove_finder_info("/path")
    assert listxattr.called
    assert listxattr.call_args == call("/path")
    assert removexattr.called
    assert removexattr.call_args == call("/path", "com.apple.FinderInfo")


@patch("xattr.removexattr")
@patch("xattr.listxattr", return_value=[])
def test_remove_finder_info_if_there_is_no_finder_info(listxattr, removexattr):
    tags._remove_finder_info("/path")
    assert listxattr.called
    assert listxattr.call_args == call("/path")
    assert removexattr.called is False


@patch("tags._remove_finder_info")
@patch("xattr.setxattr")
def test_set_all_with_tag_objects(setxattr, _remove_finder_info):
    tags.set_all(CLEAN_TAGS, file="/path")
    assert _remove_finder_info.called
    assert _remove_finder_info.call_args == call("/path")
    assert setxattr.called
    assert setxattr.call_args == call(
        "/path", "com.apple.metadata:_kMDItemUserTags", CLEAN_PLIST
    )


@patch("tags._remove_finder_info")
@patch("xattr.setxattr")
def test_set_all_with_raw_tag_strings(setxattr, _remove_finder_info):
    tags.set_all(RAW_TAGS, file="/path")
    assert _remove_finder_info.called
    assert _remove_finder_info.call_args == call("/path")
    assert setxattr.called
    assert setxattr.call_args == call(
        "/path", "com.apple.metadata:_kMDItemUserTags", CLEAN_PLIST
    )


@patch("tags.set_all")
def test_remove_all(set_all):
    tags.remove_all("/path")
    assert set_all.called
    assert set_all.call_args == call([], file="/path")
