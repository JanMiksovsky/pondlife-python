This is a Python port of a simple sample blog. The goal is to explore the representation of a site as a lazy tree of resources whose interior nodes are `Mapping` instances and whose leaf nodes are text, image, or other web resources.

## Installation

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Run the server locally

Start the server locally with:

```console
$ python3 -m src serve
```

This starts a server, e.g., on `127.0.0.1:8000`. The site is _lazy_: it only generates a resource when you ask for it.

## Build the static files

To build the static files:

```console
$ python3 -m src build
```

This creates an output folder `build`, then walks the entire site tree and writes all the resources to that folder.
