# RoboEmotion
emotion expressing for robotic arms

# Installation
This package is published and distributed as `roboemotion` [on PyPI](https://pypi.org/project/roboemotion/). \
Use `pip` to install:
```sh
$ pip install roboemotion
```

# Quick Start
The core of this package is the `RoboEmotion` class, and its instantiation really simple:
```py
from roboemotion import RoboEmotion
robo_emotion = RoboEmotion()
```

By default, the `RoboEmotion` class is instantiated with a `StandardErrorCorrespondent`. \
That being said, the servo positions are dumped into `stderr`.

In addition to `StandardErrorCorrespondent`, we also implemented `SerialCorrespondent`.
You can instantiate a `RoboEmotion` object with an existed correspondent object.

```py
from roboemotion.util import SerialCorrespondent
robo_emotion = RoboEmotion(
    correspondent=SerialCorrespondent('<SERIAL_IDENTIFIER>', baudRate=9600)
)
```

> Please note that all correspondent classes are implemented in `roboemotion.util`,
> and you need to import them before using.

Once you have a RoboEmotion object, you can perform arm movements of our emotion vocabulary with high-level API calls:
```py
robo_emotion.performEmotion('happy')
```
