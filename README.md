# Terminal Pong
An implementation of the classic 'Pong' game that runs in a terminal.

<p align="center">
   <img src="https://github.com/lbowes/ascii_pong/blob/master/gifs/gameplay.gif">
</p>

***

This project was completed as part of the 'Programming of Microcontrollers' module at the University of York. It involved interfacing two hardware gamepads to a Raspberry Pi, to control a game of Pong.
Each controller had a variable resistor dial and two buttons. The game had to run entirely on the Raspberry Pi and the game's UI was drawn by sending escape sequences over a serial line to a terminal running on a PC.

## Additional features
* GUI scales to any terminal size

<p align="center">
   <img src="https://github.com/lbowes/ascii_pong/blob/master/gifs/small.png">
</p>

* Player scores scale to values with multiple digits

<p align="center">
   <img src="https://github.com/lbowes/terminal_pong/blob/master/gifs/high_scores.png">
</p>


* Spin effect added during ball and paddle collision allowing players to cancel the ball's vertical velocity
* Floating point internal state representation
