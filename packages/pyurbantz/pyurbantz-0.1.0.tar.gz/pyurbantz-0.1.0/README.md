# pyurbantz

A Python package to help with an undocumented API of UrbanTZ.

The UrbanTZ company provides a delivery management platform of the same name
for other companies. To provide delivery tracking to their customers, those
companies can send links to a tracking page on UrbanTZ's website, which uses
a unique delivery ID in the URL to show tracking information.

Those tracking pages perform requests to an undocumented API endpoint with this
tracking ID. The endpoint provides much more information than what is actually
used in the pages; this package aims to provide a Python interface to help
creating better tracking interfaces.

## Requirements

This package just needs [requests](https://python-requests.org). That's it.

## Scripts

This package provides a simple tracker script, `urbantz.tracker`, that can be
invoked like this:

``` bash
python -m urbantz.tracker <ID> [-f|--frequency <seconds>]
```

The script will perform a request every 10 seconds (by default) to the
UrbanTZ API, then print the current date, time, and distance between the
delivery truck and the destination.

## Development

### Setup

Sample setup using
[`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/):

```
mkvirtualenv pyurbantz -a .
pip install -e .[dev]
```

### Linting

The source code follows the PEP 8 code style and performs CI checks using the
`flake8` tool. To perform the same checks locally, run `flake8` on the root
directory of this repository.
