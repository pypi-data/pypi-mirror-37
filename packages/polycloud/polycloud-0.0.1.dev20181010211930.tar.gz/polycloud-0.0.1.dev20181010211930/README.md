# Manage your open polycloud platform.

The polycloud CLI includes all features to manage your polycloud setup including service template, UI templates, platform template and operation tasks. This means you save time developing and hava a higher convinince then using multiple scripts. 

## Getting Started

Install the cli using `pip install polycloud`. Get an overview of all `<objects>` and `<commands>` using `polycloud -h`.

### Prerequisites

Install Python and Pip. 

```bash
brew install python
```

Install `cement` framework and its dependencies

```bash
pip install -r requirements.txt
```

## Installation

Install the python code for the CLI 

```bash
pip install setup.py
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run polycloud cli application

$ polycloud --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Polycloud`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it polycloud --help
```
