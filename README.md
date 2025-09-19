This is a simple blog site built using lazy Python maps.

The goal is to explore the representation of a site as a lazy tree of resources whose interior nodes are `Mapping` instances and whose leaf nodes are text, image, or other web resources. The same lazy tree is used in two rather different ways:

1. The tree can be directly served, e.g., locally for development.
2. The tree can be copied to static files for deployment to a static file server.

This demo applies ideas from the [Web Origami](https://weborigami.org) project to create a small library of mapping operations in the `map_origami` package.

[Live demo](https://pondlife-python.netlify.app)

## Installation

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
```

## Run the server locally

Start the server locally with:

```console
$ demo serve
```

This starts a server, e.g., on `127.0.0.1:8000`. The site is _lazy_: it only generates a resource when you ask for it.

## Build the static files

To build the static files:

```console
$ demo build
```

This creates an output folder `build`, then walks the entire site tree and writes all the resources to that folder.
