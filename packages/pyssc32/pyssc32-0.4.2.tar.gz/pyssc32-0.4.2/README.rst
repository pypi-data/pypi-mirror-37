.. -*- mode: rst -*-

=======
PySSC32
=======

This is simple interface to control RC servos with an SSC32 board.

Features:

- Direct and grouped queries (`#<N>P<US>` and `<SERVO_POS>...T<MS>`)
- Angle (degrees or radians) to microsecond position calculation
- Simple configuration file that help to map board output pin to servo name and provide limits.
- Sequences scripts (in YAML format)


Example
=======

::

    >>> import ssc32
    >>> import math
    >>> ssc = ssc32.SSC32('/dev/ttyUSB0', 115200, count=32)
    >>> ssc[2].position = 2000
    >>> ssc[3].name = 'pan'
    >>> ssc[4].name = 'tilt'
    >>> pan_servo = ssc['pan']
    >>> tilt_servo = ssc['tilt']
    >>> pan_servo.degrees = 0
    >>> tilt_servo.radians = math.pi/4
    >>> ssc.commit(time=1000)
    >>> ssc.is_done()
    False
    >>> ssc.is_done()
    True
    >>> ssc.description = 'My camera's pan/tilt'
    >>> ssc.save_config('my_pantilt.cfg')

