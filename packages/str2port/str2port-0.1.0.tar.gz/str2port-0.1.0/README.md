# str2port

Convert string to md5 hash, then to port numbers. No randomization involved.

Every time you run the script, it will return the same port numbers.

## Installation

```commandline
pip install str2port
```

## Usage

`str2port` is available is a CLI app,

```commandline
$ str2port --help
Usage: str2port [OPTIONS] STRING

Options:
  --use-iana  Exclude used ports from IANA list (default: false)
  --help      Show this message and exit.
$ str2port imserv
29635 44619 3226 6562 52589 12473 1423 1026
$ str2port imserv
29635 44619 3226 6562 52589 12473 1423 1026
```

Of course, it is also accessible via a Python script

```python
>>> from str2port import str2port
>>> str2port('imserv')
[29635, 44619, 3226, 6562, 52589, 12473, 1423, 1026]
```
