# piservopantilt

[![Build Status](https://travis-ci.org/kangasta/piservopantilt.svg?branch=master)](https://travis-ci.org/kangasta/piservopantilt)

Initial code to control Raspberry Pi with camera setup on 2-axis servo controlled arm.

## Usage

```python
from piservopantilt import ServoControl

s = ServoControl(pan_limits=(650,2500),tilt_limits=(650,2250))

# Move to 0,0
s.min()

# Move to 180,180
s.max()

# Move to specific coordinates
s.move_to(180,0)
```

## Testing

Run unit tests with command:

```bash
python3 -m unittest discover -s piservopantilt/tst/
```

Get test coverage with commands:
```bash
coverage run -m unittest discover -s piservopantilt/tst/
coverage report -m
```
