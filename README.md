# conversation-parser

A python utility for parsing Excel files containing conversation flows for RapidFlow into JSON objects.

## How to Run

At root directory there exist `conversation_parser.py` which requires path of excel file
and sheet name to work with. Currently it's parsing `example_story1` sheet only.

## Quickstart (windows)

1. Install requirements

```
pip install -r requirements.txt
```

2. Run tests

```
py -m pytest
```

or with coverage

```
py -m pytest --cov --cov-report html
```

## Useful Links

- [Setup python for VSCode](https://code.visualstudio.com/docs/python/python-tutorial)
