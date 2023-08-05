# legos.fact-sphere

[![Travis](https://img.shields.io/travis/drewpearce/legos.fact_sphere.svg)]() [![PyPI](https://img.shields.io/pypi/pyversions/legos.fact_sphere.svg)]() [![PyPI](https://img.shields.io/pypi/v/legos.fact_sphere.svg)]()

[![PyPI](https://img.shields.io/pypi/wheel/legos.fact_sphere.svg)]() [![PyPI](https://img.shields.io/pypi/l/legos.fact_sphere.svg)]() [![PyPI](https://img.shields.io/pypi/status/legos.fact_sphere.svg)]()

Fetch a random "fact" from the Portal2 Fact Sphere

## Usage

- `!fact` returns a random fact

## Installation
You can install locally (by cloning the repo) or from PyPi
### Local
cd into the current directory
`pip3 install .`

### From PyPi
`pip3 install legos.fact_sphere`

### Add to Legobot
This is a Lego designed for use with [Legobot](https://github.com/Legobot/Legobot), so you'll get Legobot along with this. To deploy it, import the package and add it to the active legos like so:

```python
# This is the legobot stuff
from Legobot import Lego
# This is your lego
from legos.fact_sphere import FactSphere

# Legobot stuff here
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

# Add your lego
baseplate_proxy.add_child(FactSphere)
```

## Tweaking

While you can use this one as-is, you could also add a localized version to your Legobot deployment by grabbing [fact_sphere.py](legos/fact_sphere.py) and deploying it as a local module. [Example of a Legobot instance with local modules](https://github.com/voxpupuli/thevoxfox/)

## Contributing

As always, pull requests are welcome.