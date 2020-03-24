import math
import time
from timeit import default_timer as timer
import numpy as np
from Constants import *
from Controller import Controller

if(PLATFORM_PI):
    from hardware.ControllerInterface import HardwareControllerInterface
else:
    from hardware.ControllerInterface import VirtualControllerInterface

from Ball import Ball
from Paddle import Paddle
from Display import Display
from hardware.LEDDisplay import LEDDisplay
from DrawingUtils import *
from Player import *


class Pong:


    MAX_SCORE = 30
    PHYSICS_SPEED = 1.0
    DISPLAY_WINNER_DURATION = 4.0


    def __init__(self):
        self._dt = 0.0
        self._time_s = 0.0
        self._game_won = False
        self._game_won_time_s = 0.0

        if(PLATFORM_PI):
            self._controller_interface = HardwareControllerInterface()
        else:
            self._controller_interface = VirtualControllerInterface()

        self._display = Display()
        dims = self._display.window_dims
        self._player_1 = Player(Side.LEFT, dims)
        self._player_2 = Player(Side.RIGHT, dims)
        self._ball = Ball(dims[0] / 2)

        self._serve_count = 0
        self._serving_player = self._player_1
        self._winning_player = self._player_1


    def run(self):
        self._initialise()
        running = True

        while(running):
            game_should_end = self._game_won and (self._time_s > self._game_won_time_s + Pong.DISPLAY_WINNER_DURATION)

            if(game_should_end):
                running = False

            frame_start_time = timer()

            self._handle_input()
            self._update(self._display.window_dims)
            self._draw()

            self._dt = (timer() - frame_start_time) * Pong.PHYSICS_SPEED

        self._shutdown()


    def _initialise(self):
        self._serving_player.set_as_serving()


    def _handle_input(self):
        self._controller_interface.update(self._dt)

        # Player 1 controller
        p1_dial_rot_0_1 = self._controller_interface.get_dial1_pos()
        p1_l_button_down = self._controller_interface.is_con1_but1_down()
        p1_r_button_down = self._controller_interface.is_con1_but2_down()
        self._player_1.update_controller_state(p1_dial_rot_0_1, p1_l_button_down, p1_r_button_down)

        # Player 2 controller
        p2_dial_rot_0_1 = self._controller_interface.get_dial2_pos()
        p2_l_button_down = self._controller_interface.is_con2_but1_down()
        p2_r_button_down = self._controller_interface.is_con2_but2_down()
        self._player_2.update_controller_state(p2_dial_rot_0_1, p2_l_button_down, p2_r_button_down)


    def _update(self, window_dims):
        self._time_s += self._dt

        # Update ball
        paddles = [self._player_1.paddle, self._player_2.paddle]
        self._ball.update(self._display.window_dims, paddles, self._dt)

        # Update players
        self._player_1.update(self._ball, window_dims[1], self._dt)
        self._player_2.update(self._ball, window_dims[1], self._dt)

        # Scoring
        if(self._ball.colliding_with_side_wall):
            self._updateScores()

        # Check for winner
        if(not self._game_won):
            self._check_win_condition()

        # Debug data to host console
        if(PLATFORM_PI and not PRINT_TO_TERMINAL):
            self._print_debug_info()


    def _updateScores(self):
        scoring_player = self._player_1 if self._ball.wall_collision_side == self._player_2.side else self._player_2
        scoring_player.increment_score()
        self._serve_count += 1

        # Serving
        if(self._serve_count % 5 == 0):
            self._serving_player = self._player_1 if self._serving_player == self._player_2 else self._player_2

        self._serving_player.set_as_serving()


    def _check_win_condition(self):
        self._game_won_time_s = self._time_s

        if(self._player_1.score >= Pong.MAX_SCORE):
            self._game_won = True
            self._winning_player = self._player_1
            return

        if(self._player_2.score >= Pong.MAX_SCORE):
            self._game_won = True
            self._winning_player = self._player_2


    def _print_debug_info(self):
        lines = [
            "Controller 1:",
            "   buttons:",
            "       left: -- %s",
            "       right: - %s",
            "   dial: ------ %f",
            "Left paddle:",
            "   pos: ------- %.2f",
            "   yVel: ------ %.2f",
            "   size: ------ %.2f",
            "   state: ----- %s",

            "Controller 2:",
            "   buttons:",
            "       left: -- %s",
            "       right: - %s",
            "   dial: ------ %f",
            "Right paddle:",
            "   pos: ------- %.2f",
            "   yVel: ------ %.2f",
            "   size: ------ %.2f",
            "   state: ----- %s",
            "Ball:",
            "   pos: ------ [%.2f, %.2f]",
            "   vel: ------ [%.2f, %.2f]"
        ]

        w = self._display.window_dims

        output = "\033[2J"

        for line_idx in range(len(lines)):
            output += move_cursor_code([1, line_idx + 1], w) + lines[line_idx]

        ball_vel = self._ball.getVel()
        paddles = [self._player_1.paddle, self._player_2.paddle]
        controllers = [self._player_1.controller, self._player_2.controller]

        print(output % (
            "DOWN" if controllers[0].is_button_down(Side.LEFT) else "UP",
            "DOWN" if controllers[0].is_button_down(Side.RIGHT) else "UP",
            controllers[0].get_dial_position_0_1(),
            paddles[0].get_pos()[1],
            paddles[0].get_vertical_Vel(),
            paddles[0].get_size(),
            "DOUBLE" if paddles[0].is_size_boost_active() else "NORMAL",
            "DOWN" if controllers[1].is_button_down(Side.LEFT) else "UP",
            "DOWN" if controllers[1].is_button_down(Side.RIGHT) else "UP",
            controllers[1].get_dial_position_0_1(),
            paddles[1].get_pos()[1],
            paddles[1].get_vertical_Vel(),
            paddles[1].get_size(),
            "DOUBLE" if paddles[1].is_size_boost_active() else "NORMAL",
            self._ball.pos[0], self._ball.pos[1],
            ball_vel[0], ball_vel[1])
        )


    def _draw(self):
        # Terminal display
        self._display.begin()

        dims_x = self._display.window_dims[0]
        if(not self._game_won):
            self._display.draw_net()
            self._display.draw_score(self._player_2.score, [int(dims_x * 0.75), 4])
            self._display.draw_score(self._player_1.score, [int(dims_x * 0.25), 4])
            self._display.draw_player(self._player_1)
            self._display.draw_player(self._player_2)
            self._display.draw_ball(self._ball)
        else:
            self._display.draw_win_screen(self._winning_player)

        self._display.end()

        # LED displays
        if(PLATFORM_PI and LEDS_USED):
            self._led_display.set_leds(float(self._ball.pos[0] / dims_x))


    def _shutdown(self):
        self._display.close()


def main():
    pong = Pong()
    pong.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pong.shutdown()
        print(colour_reset_code())
        print(cursor_visibilty_code())
