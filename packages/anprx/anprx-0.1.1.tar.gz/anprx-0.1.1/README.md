[![PyPI version](https://badge.fury.io/py/anprx.svg)](https://badge.fury.io/py/anprx)
[![Build Status](https://travis-ci.org/PedrosWits/anprx.svg?branch=master)](https://travis-ci.org/PedrosWits/anprx)
[![Documentation Status](https://readthedocs.org/projects/anprx/badge/?version=latest)](https://anprx.readthedocs.io/en/latest/?badge=latest)

# ANPRx

Traffic analysis using networks of Automatic Number Plate Recognition cameras.

## Installation

ANPRX is available through pypi:
```
pip install anprx
```

See `requirements.txt` for a complete list of dependencies.

**Important:**
[OSMnx](https://github.com/gboeing/osmnx) requires the [Rtree](http://toblerity.org/rtree/) package which is a python wrapper for [libspatialindex](https://libspatialindex.github.io/). To get osmnx to work properly, which this package heavily relies on,  [download and install](.travis.yml) [libspatialindex](https://libspatialindex.github.io/) first.

## Usage Example

```python
import anprx

# Using the same dummy location twice
locations = [ anprx.Point(lat = 54.974537,
                          lng = -1.625644),

              anprx.Point(lat = 54.974537,
                          lng = -1.625644)
            ]

network = anprx.get_surrounding_network(locations)

# With address filtering
mock_camera1 = anprx.Camera(
  network = network,
  id = "c1",
  point = locations[0],
  address = "Pitt Street, Newcastle Upon Tyne, UK",
  filter_by_address = True)

mock_camera1.plot()

# Without address filtering
mock_camera2 = anprx.Camera(
  network = network,
  id = "c2",
  point = locations[1])

mock_camera2.plot()
```

Mock camera on Pitt Street with address filtering |  Mock camera on Pitt Street without address filtering
:-------------------------:|:-------------------------:
![not a real camera, sorry :()](docs/_static/mock_camera_1.png)  |  ![not a real camera, sorry :(](docs/_static/mock_camera_2.png)

## Features

### Stable

Given the pair of latitude and longitude coordinates of each camera, you can:

- Obtain a model of the drivable street network, using [osmnx](https://github.com/gboeing/osmnx) and [networkx](https://networkx.github.io/documentation/stable/index.html), that encompasses the cameras (coordinate points).
- Compute the likelihood of neighbouring edges (road segments) as the true edge observed by the camera. Filter out candidate edges by address.
- Visualise the camera's placement on the road network, including nearby nodes, and the likelihood of candidate edges.

### Under development

Among others:

- Enrich the road network by adding further attributes to the edges (address details, elevation, bearing).
- Filter/compress the road network based on edge attributes.
- Batch analysis of ANPR data: trip identification and inference.

## Documentation

All modules and methods are documented in [anprx.readthedocs.io](https://anprx.readthedocs.io/en/latest/)

## License
[Apache v2.0](LICENSE)
