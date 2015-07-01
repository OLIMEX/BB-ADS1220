================================
Olimex BB-ADS1220 python example
================================
Description
-----------
BB-ADS1220_ is four channel sigma-delta precise 24-bit adc breakboard.

ADS1220 features two differential or four single-ended inputs through a flexible input multiplexer (MUX), a low-noise,
programmable gain amplifier (PGA), two programmable excitation current sources, a voltage reference, an oscillator, a
low-side switch, and a precision temperature sensor.

FEATURES:

- Fully integrated TI ADS1220
- All IC pins available at the two connector rows
- Each signal is named near the connector
- Breadboard-friendly 0.1" step between pins
- Included plastic headers for easier mounting on a breadboard (not soldered to the board)
- Board dimensions: (750 x 850)mil ~ (19.0 x 21.5)mm

Texas Instruments ADS1220 features:

- Low Current Consumption 120 µA in Duty-Cycle Mode
- Wide Supply Range: 2.3 V to 5.5 V
- Programmable Gain: 1 V/V to 128 V/V
- Programmable Data Rates: Up to 2 kSPS
- Up to 20-Bits Effective Resolution
- Simultaneous 50-Hz and 60-Hz Rejection at 20 SPS with Single-Cycle Settling Digital Filter
- Two Differential or Four Single-Ended Inputs
- Dual Matched Programmable Current Sources: 10 µA to 1.5 mA
- Internal 2.048-V Reference: 5 ppm/°C (typ) Drift
- Internal 2% Accurate Oscillator
- Internal Temperature Sensor: 0.5°C (typ) Accuracy
- SPI-Compatible Interface (Mode 1)

Connection
----------

::

                            ---------------------------------
                            |                               |
                  UEXT(2) - | AVSS                      VDD | - UEXT(1)
                            |                               |
                          - | IN0                     DRDY# | - GPIO3(5)
                            |                               |
                          - | IN1                       CS# | - UEXT(10)
                            |                               |
                          - | IN2                       CLK | - UEXT(9)
                            |                               |
                          - | IN3                       DIN | - UEXT(8)
                            |                               |
                  UEXT(1) - | AVDD                     DOUT | - UEXT(7)
                            |                               |
                          - | REFP                      GND | - UEXT(2)
                            |                               |
                          - | REFN                     AVSS | - UEXT(2)
                            |                               |
                            ---------------------------------

This is minimum required wiring. The signal DRDY# is optional.
Instead of polling it you can just wait some time to be sure that conversation is completed. Also
you can use any available pin. In this example we use GPIO3(5) which is *PH0*.


Running
-------
Download both files (**main.py** and **ADS1220.py**) to some folder, for example ~/ads and run them like this:

::

    cd ~/ads
    python main.py

You should see something like this:

::

    Temperature: 25.53125 C
    AVDD: 3.359197V

*Note*: If you have any issues run these commands:

::

    apt-get update
    apt-get install python-dev python-pip
    pip install --upgrade pyA20

API
----
See *ADS1220* class for detailed information

About
-----

:Author: Stefan Mavrodiev
:Organization: OLIMEX Ltd.
:Contact: support@olimex.com
:Version: 1.0
:Date: 1 JUL 2015


.. _BB-ADS1220: https://www.olimex.com/Products/Breadboarding/BB-ADS1220/open-source-hardware

