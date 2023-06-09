"""CSC111 Winter 2023 Project: Connect 4 (Main)

Module Description
==================

This module contains the codes that are necessary to run the entire program from start to finish.
By reading the codes of this file, you can gain insights into the
role and functionality of these codes
as well as how they contribute to this project as a whole.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the
Teaching Stream of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.
This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
"""
from __future__ import annotations
import sys
import pygame
from runner import GameRunner, run_game_interactive, run_game_between_ai
from constant import WINDOW_WIDTH, WINDOW_HEIGHT


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # Disabled 'unused-import' because you can use them by uncommenting some sections of code in main
    # for different purposes.

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4,
    #     'extra-imports': ['__future__', 'sys', 'pygame', 'runner', 'constant'],
    #     'disable': ['unused-import'],
    # })

    # The following section of code allows you to play against our Greedy AI Player in a Pygame window.
    # =================================================================================================================
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.flip()
    pygame.display.set_caption("CONNECT FOUR")
    clock = pygame.time.Clock()

    game_runner = GameRunner(5)

    # Plays background music
    pygame.mixer.music.load('waterfall.mp3')
    pygame.mixer.music.play(-1)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            game_runner.handle_event(event, screen)

        game_runner.draw(screen)
        pygame.display.update()
        clock.tick(50)

    # The following code allows you to play against any AI of your choice in the console.
    # =================================================================================================================
    # while True:
    #     run_game_interactive()

    # The following code runs games between two of our AIs by your choice.
    # You will be guided by instructions in the console to choose the two AIs.
    # =================================================================================================================
    # while True:
    #     run_game_between_ai()
