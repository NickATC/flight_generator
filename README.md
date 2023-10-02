# flight_generator - FlightGen!©
A program for pilot students who want to train IFR procedures.  FlightGen!© will generate flights that comply with specific characteristics based on pilot training requirements.  What to fly a DME arc on departure and arrival, but only have 45 minutes available to train??  FlightGen! has you covered!

iOS version under development!

*Version 1.3   May 2020*

Sometimes my students asked me for flights to practice in the simulator with certain requirements (for example: airports with arc on departure or arrival, with ILS approach, or airports with certain difficulty), and I ended up suggesting the same flights over and over again…so I decided to write a program where my students could select the options and based on them my program would suggest flights.

That’s how Flight Gen!© was born. Several other options were added, for example suggestions based on the time you have available for the flight, this way, if you have only 30 minutes in the KingAir 350, Flight Gen!© will select one flight for you… as simple as that!

This program is for all my students. 

I hope you find it useful…and practice until you can navigate with no errors.

## What this program is going to do?
This program will suggest a flight for you based on your selected options.

Once the flight is suggested, it will give you very basic airport information like ICAO codes, runways available, runway length, course and distance and EET to your destination, and some other info.

All suggested flights will be in Colombia.

## Prerequisites

To run the program properly you need Windows OS, Python 3.7+ and you just need to install pillow

To install:
```
pip install pillow
```
You should be ready within seconds!


## Getting Started

1.  Download the repo.
2.  Run *main.py*
3.  Read the manual:   flightGen_guide.pdf  It can be accessed thru the GUI or just click on the document above.


### Things to fix
The DB queries can be improved.  They work perfectly, but can be written in a better way.
Some tooltips can be implemented. 
Adapt the GUI to Mac and Linux OS.

## Authors

* **Nicolás Táutiva** - *Initial work* - [NickATC](https://github.com/NickATC)

## Acknowledgments

* Thanks to PurpleBooth article on how to create a good README [Here](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/824da51d0763e6855c338cc8107b2ff890e7dd43/README-Template.md) 
