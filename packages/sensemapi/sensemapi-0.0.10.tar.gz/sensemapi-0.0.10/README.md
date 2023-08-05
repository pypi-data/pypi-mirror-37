# SenseMAPI - Pythonic access to the OpenSenseMap API

[![pipeline status](https://gitlab.com/tue-umphy/python3-sensemapi/badges/master/pipeline.svg)](https://gitlab.com/tue-umphy/python3-sensemapi/commits/master) [![coverage report](https://gitlab.com/tue-umphy/co2mofetten/python3-sensemapi/badges/master/coverage.svg)](https://tue-umphy.gitlab.io/python3-sensemapi/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://tue-umphy.gitlab.io/python3-sensemapi/) [![PyPI](https://badge.fury.io/py/sensemapi.svg)](https://badge.fury.io/py/sensemapi)

`sensemapi` is a Python package to access the [OpenSenseMap
API](https://api.opensensemap.org).

> ## Disclaimer
>
> This software was developed within the context of a
> [CO2 monitoring project](https://gitlab.com/tue-umphy/co2mofetten)
> of the University of Tübingen, Germany. The developer is not in any
> way affiliated with the [senseBox project](https://www.sensebox.de/en/).

## What can `sensemapi` do?

With `sensemapi`, you can do the most important things that you can also do via
the [OpenSenseMap user interface](https://opensensemap.org).

See some examples:

### Access an OpenSenseMap account

```python
account = sensemapi.account.SenseMapAccount(
    email = "SENSEMAP_EMAIL",
    password = os.environ.get("SENSEMAP_PASSWORD")
    )
```

### Create new senseBoxes

```python
# set up a senseBox (offline)
box = sensemapi.senseBox.senseBox(
    exposure = "outdoor",
    name="My senseBox",
    current_lat=50.5,
    current_lon=10.1)
# add a temperature sensor to the box (offline)
box.new_sensor(
    title="temperature",
    unit="°C",
    type="SHT31",
    icon="osem-temperature-celsius")
# create the senseBox (online)
account.new_box(box)
```

### Modify senseBoxes and sensors

```python
# retreive the account's boxes
account.get_own_boxes()
# choose the first box
box = account.boxes[0]
# change the box
box.name = "My supercool senseBox"
# ... do anything with the box object ...
# upload the changes
box.upload_metadata()
```

### Upload measurements

```python
# select the box's first sensor
sensor = box.sensors[0]
# reset the time to use the current time
sensor.last_time = None
# specify measurement value
sensor.last_value = 25.2
# upload the measurement
sensor.upload_measurement()
```

### Delete a senseBox

```python
# delete the account's first senseBox
account.delete_box(account.boxes[0].id, really=True)
```

### Retreive any senseBox by its ID

```python
# with an account
account.get_box(id = "57000b8745fd40c8196ad04c")
# without an account
sensemapi.client.SenseMapClient().get_box(id = "57000b8745fd40c8196ad04c")
```

### Retreive measurements of a senseBox sensor

```python
# get a box
box = sensemapi.client.SenseMapClient().get_box(id="57000b8745fd40c8196ad04c")
# the box' first sensor
sensor = box.sensors[0]
# get the sensor's latest measurements as pandas.Series
series = sensor.get_measurements().series
```

More features are likely to follow...

## Installation

The `sensemapi` package is best installed via `pip3`. Run from anywhere:

```bash
pip3 install --user sensemapi
pip3 install --user pandas # if you want pandas support
```

This downloads and installs the package from the [Python Package
Index](https://pypi.org).

You may also install `sensemapi` via `pip3` from the repository root:

```bash
pip3 install --user .
```

## Documentation

Documentation of the `sensemapi` package can be found [here on
GitLab](https://tue-umphy.gitlab.io/python3-sensemapi/).

## Development

The following might only be interesting for developers

### Tests

Since this is an API library, you need to specify an account to run the tests:

```bash
export SENSEMAP_EMAIL="user@email.com"   # specify either the email...
export SENSEMAP_USER="username"          # or the username
export SENSEMAP_PASSWORD="5uP3rP45sW0Rd"
```

You may also specifiy this sensitive data in a file which can then be
`source`d.

To run the test suite, run from the repository root

```bash
./setup.py test
```

To get a test coverage, run

```bash
make coverage
```
