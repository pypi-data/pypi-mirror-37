v0.0.8 (2018-10-10)
======================

- add class for applications using sensemapi

v0.0.7 (2018-09-28)
======================

- implement cache for authentication
- implement transparent handling of both email and username
- fix bug with setting location when retrieving a box
- add uploading multiple sensor measurement of a senseBox at once

v0.0.6 (2018-09-19)
======================

- drop iso8601 dependency
- make pandas an optional dependency
- add changelog to the RPM package

v0.0.5 (2018-09-15)
======================

- handle HTTP 429 "Too Many Requests"-errors by waiting and retrying
- fix a bug in uploading a sensor measurement of "0" value
- add deletion of sensor measurements

v0.0.4 (2018-08-29)
======================

- add retrieval of sensor measurement timeseries
- improve test suite

v0.0.3 (2018-08-28)
======================

- simplify deletion of a sensor from a senseBox
- update documentation

v0.0.2 (2018-08-27)
======================

- fix README Markdown rendering on PyPi

v0.0.1 (2018-08-27)
======================

- initial version with basic functionality
    - account sign in/out
    - handling authentication tokens
    - creating senseBoxes/sensors
    - uploading senseBoxes/sensors
    - modifying senseBoxes/sensors
    - posting sensor measurements
    - documentation
