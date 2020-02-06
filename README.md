# Use tags to organize files on Mac from Python

![Release](https://github.com/dmkskn/macos-tags/workflows/Release/badge.svg)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Installation

```bash
pip install macos-tags
```

Works since Python 3.7.

## Tutorial

Get all tags:

```python
>>> import macos_tags


>>> macos_tags.tags()
[Tag(name='design', color=None), ..., Tag(name='python', color=<Color.GREEN: 2>]
```

Get files by tag name:

```python
>>> macos_tags.find("design")
['/Users/home/apple.jpg', '/Users/home/WEB_POSTERS.png']
```

Count files by tag name:

```python
>>> macos_tags.count("design")
2
```

List the tags on the file:

```python
>>> path = "/path/to/file"

>>> macos_tags.get_all(path)
[Tag(name='design', color=None), Tag(name='python', color=<Color.GREEN: 2>]
```

Add a tag to file:

```python
>>> macos_tags.add("design", file=path)
```

> When using `str` objects to define a tag, if a tag does not exist in the system, it will be added without a color label.

Add a new color tag by using `Tag` data class and `Color` enumeration:

```python
>>> from macos_tags import Tag, Color


>>> tag = Tag(name="python", color=Color.GREEN)

>>> macos_tags.add(tag, file=path)
```

Add a new color tag using the `str` object, where the tag name and color number (from 1 to 7) are separated by the literal `\n`:

```python
>>> tag = f"python\n{Color.GREEN}"  # == "python\n2"

>>> macos_tags.add(tag, file=path)
```

> If the tag already exists in the system with a different color, the new color will be ignored.

Remove tag from file:

```python
>>> macos_tags.remove(tag, file=path)
```

Remove all tags from a file at once:

```python
>>> macos_tags.remove_all(path)
```

Change all tags in the file:

```python
>>> macos_tags.get_all(path)
[Tag(name='design', color=None), Tag(name='python', color=<Color.GREEN: 2>]

>>> new_tags = [Tag("book"), Tag("programming", Color.BLUE)]

>>> macos_tags.set_all(new_tags, file=path)

>>> macos_tags.get_all(path)
[Tag(name="book", color=None), Tag("programming", <Color.BLUE: 4>]
```

❤️