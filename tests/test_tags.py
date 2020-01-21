from unittest.mock import call, patch

import tags


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
