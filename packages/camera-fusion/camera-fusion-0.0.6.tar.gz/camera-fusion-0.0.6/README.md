[![PyPI version](https://img.shields.io/pypi/v/camera-fusion.svg)](https://pypi.python.org/pypi/camera-fusion/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/camera-fusion.svg)](https://pypi.python.org/pypi/camera-fusion/)
[![PyPI status](https://img.shields.io/pypi/status/camera-fusion.svg)](https://pypi.python.org/pypi/camera-fusion/)
[<img src="https://cdn.rawgit.com/a1rb4Ck/camera-fusion/master/tests/reports/coverage.svg" with="100%" height="20">](https://htmlpreview.github.io/?https://raw.githubusercontent.com/a1rb4Ck/camera-fusion/master/tests/reports/coverage-html/index.html)
[![PyPI license](https://img.shields.io/pypi/l/camera-fusion.svg)](https://pypi.python.org/pypi/camera-fusion/)  

camera-fusion
==========

Multiple cameras correction calibration and fusion with OpenCV Python.
This package use ChAruco board to achieve accurate multi-cameras fusion.

Installation
----------

```bash
pip install camera-fusion
```
Depending of your environment, you could have to compile OpenCV from source with Python bindings.


Quickstart
----------

### Calibration
Print a [ChAruco board](https://www.uco.es/investiga/grupos/ava/node/26), for example the one in the *./resources* folder.

Measure the length of the Aruco marker and the length of the black chess square. Then start the calibration scripts.

### Usage examples

Generate the lens correction calibration file for a specific camera.

```bash
python3 ./bin/camera_calibration
```

Generate homographies between multiple cameras to fuse/blend on a specific plane. If no lens correction calibration exist for the cameras, they will be generate.

```bash
python3 ./bin/camera_calibration
```

Simple blending methods are implemented:
- Blue channel to RGB blending
- Gray scale to RGB blending
- Weighted blending
- Difference

Use cases
----------

This project was made to create a super low-cost degree of linear polarization imager. With three cheap repurposed webcams, we achieve decent results and frame-rate.

Development
----------

Test:

```bash
tox
```

Build:

```bash
make all
```
