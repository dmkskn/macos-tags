from unittest.mock import call, patch

import tags

RAW_PLIST = b"bplist00\xa2\x01\x02Ttag1Vtag2\n5\x08\x0b\x10\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17"
RAW_TAGS = ["tag1", "tag2\n5"]  # from plist
CLEAN_TAGS = [tags.Tag(name="tag1", color=None), tags.Tag(name="tag2", color=5)]


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
