This microservice is the gui controller for a thermostat. It listens to
input events (buttons and rotary encoders) generated e.g. by copreus. As
output it generates the desired set-point-values for the pid temperature
control (like epidaurus) and additional information needed for the
display server to generate to gui (e.g. nikippe).

The controller can handle different modes (like day/night) for manual
operation and schedules (15 minute time slots) for automatic mode.

As the circuit for the thermostat controller allows to switch between
observer and controller operation, this gui mirrors this by toggling
between active and passive. Active operation means that the DAC is
connected to the heater; passive that the DAC is disconnected by opening
the relais.

Input topics: \* set-point for temperature - up/down (string command) -
reset to default (string command) \* selector for mode - left/right
(string command) - reset to default (string command) \* active/passive
operation toggle (string command)

Output topics: \* temperature set-point (float value) \* schedule chart
image (encoded image) - see nikippe.mqttimage \* mode icon identifier
(string name) - see nikippe.imagelist \* relais control (string command)

Argeus [1]_, son of Pelops and Hippodamia, by Hegesandra father of
Alector and Boethoos. [`wiki <https://en.wikipedia.org/wiki/Argeus>`__]

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Argaeus`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

For Users
=========

Installation Core-Functionality
-------------------------------

Prerequisites for the core functionality are:

::

    sudo apt install python3 python3-pip

Install via pip:

::

    sudo pip3 install pelops argaues

To update to the latest version add ``--upgrade`` as prefix to the
``pip3`` line above.

Install via gitlab (might need additional packages):

::

    git clone git@gitlab.com:pelops/argaues.git
    cd argaeus
    sudo python3 setup.py install

This will install the following shell scripts: \* ``argaeus``

The script cli arguments are: \* '-c'/'--config' - config file
(mandatory) \* '--version' - show the version number and exit

YAML-Config
-----------

A yaml [2]_ file must contain three root blocks: \* mqtt - mqtt-address,
mqtt-port, and path to credentials file credentials-file (a file
consisting of two entries: mqtt-user, mqtt-password) \* logger - which
log level and which file to be used \* controller - mode-controller -
list of different operation modes like fixed temperature or time
schedule driven - setpoint-controller - changes the set-point of the
current program - operation-controller - turns the outgoing relais
on/off

::

    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml
        log-level: INFO

    logger:
        log-level: DEBUG
        log-file: argeus.log

    controller:
        operation-controller:  # turns the outgoing relais on/off
            default-is-active: True  # Is the controller active or passive initially
            topic-pub: /test/relais/closed  # Topic that controls the output behavior relais of the thermostat.
            command-active: ON  # set to active command - publish this value to topic-pub, to set the controller to active operation.
            command-passive: OFF  # set to passive command - publish this value to topic-pub, to set the controller to passive operation.
            topic-sub-toggle: /test/r1/button/pressed  # incoming event to toggle active/passive operation (optional together with command-toggle)
            command-toggle: PRESSED  # command for topic-sub-toggle / toggle active/passive operation (optional together with topic-sub-toggle)

        mode-controller:  # list of different operation modes like fixed temperature or time schedule driven
            default-mode: Schedule  # default mode - must be a name from modes list
            topics-sub:  # incoming topics
                to-prev: /test/r2/rotate  # select previous mode
                command-prev: LEFT  # to previous command - if this value is published to to-prev, the previous entry in the mode list is selected
                to-next: /test/r2/rotate  # select next mode
                command-next: RIGHT  # to next command - if this value is published to to-next, the next entry in the mode list is selected
                to-default: /test/r1/button/pressed  # incoming event to reset to default mode (optional together with command-default)
                command-default: PRESSED  # command for topic-sub / reset to default mode (optional together with to-default)
            topics-pub:  # outgoing topics
                display-server-schedule-image: /test/display/schedule  # topic of an nikippe-mqttimage instance
                display-server-mode-icon: /test/display/mode  # topic of an nikippe-imagelist instance
                temperature-set-point: /test/temperature/set-point  # topic of e.g. epidaurus (=pid temperature control) set-point listener
            modes:  # list of modes
                - name: Night  # unique name for mode entry
                  type: program  # program or schedule - a schedule consists of programms
                  selectable: True  # can be selected using the gui
                  set-point: 19.5  # target temperature of this mode

                - name: Day  # unique name for mode entry
                  type: program  # program or schedule - a schedule consists of programms
                  selectable: True  # can be selected using the gui
                  set-point: 23.0  # target temperature of this mode

                - name: Frost  # unique name for mode entry
                  type: program  # program or schedule - a schedule consists of programms
                  selectable: False  # can be selected using the gui
                  set-point: 5.0  # target temperature of this mode

                - name: Schedule  # unique name for mode entry
                  type: schedule  # program or schedule - a schedule consists of programms
                  selectable: True  # can be selected using the gui
                  image:  # generate image for nikippe.mqttimage
                      width: 192  # width of image
                      height: 2  # height of image
                      foreground-color: 255  # from 0 to 255.
                      background-color: 0  # from 0 to 255.
                      patterns:  # 0, 1, 2, 3 are valid patterns
                          Night: 0    # nothing
                          Morning: 1  # lower dot
                          Day: 2      # upper and lower dot
                          Frost: 3    # upper dot
                  schedule:  # definition which program is active in each 15 minute slot of a day
                      "00:00": Night
                      "00:15": Night
                      "00:30": Night
                      "00:45": Night
                        ...
                      "12:00": Day
                      "12:15": Day
                      "12:30": Day
                      "12:45": Day
                        ...
                      "23:00": Night
                      "23:15": Night
                      "23:30": Night
                      "23:45": Night

        setpoint-controller:  # changes the set-point of the current program
            topic-sub-down: /test/r1/rotate  # reduce temperature topic
            command-down: LEFT  # down command - if this value is published to topic-sub-down, temp is reduced.
            topic-sub-up: /test/r1/rotate  # increase temperature topic
            command-up: RIGHT  # up command - if this value is published to topic-sub-up, temp is increased.
            topic-sub-reset: /test/r1/button/pressed  # incoming event to reset temperature to default (optional together with command-reset)
            command-reset: PRESSED  # command for topic-sub-reset / reset to default (optional together with topic-sub-reset)
            step-size: 0.5  # Temperature is changed by step size for each rotation step.
            max-temp: 30.0  # Maximum value for temperature
            min-temp: 10.0  # Minimum value for temperature

systemd
-------

-  add systemd example.

For Developers
==============

Getting Started
---------------

The main class ``ThermostatGUIController`` is a specialication of pelops
``AbstractMicroservice`` hosts the (currently) three sub-controller
``ModeController``, ``SetPointController``, and ``OperationController``.
They must be specializations of ``AController``.

Todos
-----

-  ...

Misc
----

The code is written for ``python3`` (and tested with python 3.5 on an
Raspberry Pi Zero with Raspbian Stretch).

`Merge requests <https://gitlab.com/pelops/argaeus/merge_requests>`__ /
`bug reports <https://gitlab.com/pelops/argaeus/issues>`__ are always
welcome.

.. [1]
   Again, not an icon of the "real" Argeus. It is a picture used in the
   context of Argeus I of Macedon
   `wiki <https://en.wikipedia.org/wiki/Argaeus_I_of_Macedon#/media/File:Fragment_Maenad_Louvre_G160.jpg>`__.

.. [2]
   Currently, pyyaml is yaml 1.1 compliant. In pyyaml On/Off and Yes/No
   are automatically converted to True/False. This is an unwanted
   behavior and deprecated in yaml 1.2. In copreus this autoconversion
   is removed. Thus, On/Off and Yes/No are read from the yaml file as
   strings (see module baseclasses.myconfigtools).

