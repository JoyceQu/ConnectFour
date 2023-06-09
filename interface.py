"""CSC111 Winter 2023 Project: Connect 4 (Interface)

Module Description
==================

This module contains a collection of Python classes and functions that represent the interface of Connect 4,
which is mainly implemented using the Pygame modules.
By reading the *docstring* of this file, you can gain insights into the
role and functionality of these classes and functions
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
from typing import Optional
import pygame
from pygame import gfxdraw
from constant import UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT, \
    GRID_WIDTH, GRID_HEIGHT, SQUARESIZE, RADIUS, BORDER_RADIUS, \
    BUTTON_WIDTH, BUTTON_HEIGHT, FONT_BUTTON,\
    RED, DARK_RED, YELLOW, DARK_YELLOW, BLUE, DARK_BLUE, WHITE, GREY, DARK_GREY

# We did not import WINDOW_WIDTH, WINDOW_HEIGHT from constant because python-ta detected it as unused-import
# But we used WINDOW_WIDTH, WINDOW_HEIGHT in docstrings as a part of Preconditions.
# So, if you want to @check_contract, you may need to import these two constants.


class Button:
    """A class represents a circle buttons.
    Instance Attributes:
        - disabled: show that if the button should be disactivated
        - word: the word that is printed on the button
        - center: a tuple of integers that is the center location of the button
        - _button_color: the rgb color of the inner side of the button
        - _darker_button_color: the rgb color of the outer side of the button
        - _disabled_color: rgb color the button when self.disabled is True

    Representation Invariables:
        - 0 <= self.center[0] <= WINDOW_WIDTH
        - 0 <= self.center[1] <= WINDOW_HEIGHT
        - all(0 <= color[i] <= 255 for color in [self._button_color, self._darker_button_color, self._disabled_color]
        for i in range(3))
    """
    word: str
    center: tuple[int, int]
    disabled: bool
    _button_color: tuple[int, int, int]
    _darker_button_color: tuple[int, int, int]
    _disabled_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, word: str) -> None:
        """Create a rectangular button of given image at (x, y)
        x, y are the topleft location of the button on a surface.
        """
        self.center = (x, y)
        self.word = word
        self.disabled = False

        self._button_color = BLUE
        self._darker_button_color = DARK_BLUE
        self._disabled_color = GREY

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button with words on it on the given window.
        It doesn't update surface in this function."""

        # draw a rectangle
        topleft_x = int(self.center[0] - BUTTON_WIDTH / 2)
        topleft_y = int(self.center[1] - BUTTON_HEIGHT / 2)

        if self.disabled:
            filled_color, outline_color = self._disabled_color, self._disabled_color
        else:
            filled_color, outline_color = self._button_color, self._darker_button_color

        # draw the outer Rect
        draw_rounded_rect(surface, pygame.Rect(topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT),
                          outline_color, BORDER_RADIUS)
        # draw the inner Rect
        draw_rounded_rect(surface, pygame.Rect(topleft_x + int(BUTTON_WIDTH * 0.05),
                                               topleft_y + int(BUTTON_WIDTH * 0.05),
                          int(BUTTON_WIDTH * 0.9), int(0.85 * BUTTON_HEIGHT)),
                          filled_color, int(BORDER_RADIUS * 0.8))

        # draw word
        text = FONT_BUTTON.render(self.word, True, WHITE)
        w, h = text.get_size()
        text_x, text_y = int(self.center[0] - w / 2), int(self.center[1] - h / 2)
        surface.blit(text, (text_x, text_y))

    def is_valid_click(self, position: tuple[int, int]) -> bool:
        """Return if the given position is on the position of the button
        Preconditions:
            - 0 <= position[0] <= WINDOW_WIDTH
            - 0 <= position[1] <= WINDOW_HEIGHT
        """
        if self.disabled:
            return False

        left, right = int(self.center[0] - BUTTON_WIDTH / 2), int(self.center[0] + BUTTON_WIDTH / 2)
        up, down = int(self.center[1] - BUTTON_HEIGHT / 2), int(self.center[1] + BUTTON_HEIGHT / 2)
        if left <= position[0] <= right and up <= position[1] <= down:
            return True
        else:
            return False


class GameBoard:
    """ A class represents the 6 * 7 grid on which discs are put
    Instance Attributes:
        - x: x position on pygame screen
        - y: y position on pygame
        - disabled: whether GameBoard is activated

    Private Instance Attributes:
        - _grid: a 2D list of Disc
        - _hint_position: the position of hint disc. If no hint is given now, it is None

    Representative Invariants:
        - 0 <= self.x <= WINDOW_WIDTH
        - 0 <= self.y <= WINDOW_HEIGHT
    """
    x: int
    y: int
    disabled: bool
    _grid: list[list[Disc]]
    _hint_position: Optional[tuple[int, int]]

    def __init__(self, x: int, y: int, disabled: bool = True) -> None:
        """
        Initialize a GameBoard at position (x, y)
        """
        self.x, self.y = x, y
        self._grid = []
        self.disabled = disabled
        for grid_y in range(GRID_HEIGHT):
            row_so_far = []
            for grid_x in range(GRID_WIDTH):
                position_x, position_y = self._get_central_position(grid_x, grid_y)
                row_so_far.append(Disc(position_x, position_y, UNOCCUPIED))
            self._grid.append(row_so_far)
        self._hint_position = None

    def _get_central_position(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        """
        Return the center of the disc of self._grid[grid_x][grid_y]

        Preconditions:
            - 0 <= grid_x <= WINDOW_WIDTH
            - 0 <= grid_y <= WINDOW_HEIGHT
        """
        position_x = int(self.x + (grid_x + 0.5) * SQUARESIZE)
        position_y = int(self.y + (grid_y + 0.5) * SQUARESIZE)
        return (position_x, position_y)

    def draw(self, surface: pygame.Surface) -> None:
        """ Draw game board on the given surface
        """
        board_rect = pygame.Rect(self.x, self.y, GRID_WIDTH * SQUARESIZE, GRID_HEIGHT * SQUARESIZE)
        draw_rounded_rect(surface, board_rect, BLUE, BORDER_RADIUS)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self._grid[y][x].draw(surface)

    def is_valid_click(self, position: tuple[int, int]) -> bool:
        """ Return if the position is on the gameboard. If self.disabled is True, it is not a valid click
        Preconditions:
            - 0 <= position[0] <= WINDOW_WIDTH
            - 0 <= position[1] <= WINDOW_HEIGHT
        """
        if self.disabled:
            return False

        position_x, position_y = position
        return self.x <= position_x <= self.x + SQUARESIZE * GRID_WIDTH and \
            self.y <= position_y <= self.y + SQUARESIZE * GRID_HEIGHT

    def get_move_column(self, position: tuple[int, int]) -> int:
        """
        Return which column the position points to. Return value is [0, GRID_WIDTH - 1], inclusive
        Preconditions:
            - 0 <= position[0] <= WINDOW_WIDTH
        """
        return (position[0] - self.x) // SQUARESIZE

    def record_move(self, move_position: tuple[int, int], disc_type: int) -> None:
        """ Update the color of the disc at move_position. If disc_type is HINT, also update self._hint_position

        move_position indicates the position of disc in the order of bottom to top,
        i.e (0,0) in move_position means the bottom left corner
        whereas self._disc indicates position of disc from top to bottom,
        i.e. (0,0) in self.disc means the top left corner.

        Preconditions:
            - disc_type in [UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT]
        """
        x, y = move_position
        y = GRID_HEIGHT - 1 - y
        self._grid[y][x].update_color_and_type(disc_type)
        if disc_type == HINT:
            self._hint_position = (x, y)

    def remove_hint(self) -> None:
        """ Remove the hint disc by updating the hint disc to UNOCCUPIED, and set self._hint_position to None
        """
        if self._hint_position is not None:
            x, y = self._hint_position
            if self._grid[y][x].disc_type == HINT:
                self._grid[y][x].update_color_and_type(UNOCCUPIED)
            self._hint_position = None


class Disc:
    """ A class represent a disc on game board.
    Instance Attributes:
        - x: x position of the disc on screen
        - y: y position of the disc on screen
        - disc_type: the current type of the disc
        - filled_color: the rgb color of the inner of disc
        - outline_color: the rgb color of the outline of disc
    Representative Invariants:
        - disc_type in [UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT]
        - all(0 <= color[i] <= 255 for color in [filled_color, outline_color] for i in range (3))
    """
    x: int
    y: int
    disc_type: int
    filled_color: tuple[int, int, int]
    outline_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, disc_type: int) -> None:
        """
        Initialize a disc
        """
        self.x, self.y = x, y
        self.update_color_and_type(disc_type)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the disc on the given surface
        """
        draw_circle(surface, self.x, self.y, RADIUS, self.outline_color)
        draw_circle(surface, self.x, self.y, int(RADIUS * 4 / 5), self.filled_color)

    def update_color_and_type(self, disc_type: int) -> None:
        """
        Update the color of the disc based on the disc_type
        Preconditions:
            - disc_type in [UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT]
        """
        self.disc_type = disc_type
        if self.disc_type == UNOCCUPIED:
            self.filled_color, self.outline_color = WHITE, WHITE
        elif self.disc_type == PLAYER_ONE:
            self.filled_color, self.outline_color = RED, DARK_RED
        elif self.disc_type == PLAYER_TWO:
            self.filled_color, self.outline_color = YELLOW, DARK_YELLOW
        else:
            self.filled_color, self.outline_color = GREY, DARK_GREY


class Label:
    """ A class represents words showed on the pygame screen
    Instance Attributes:
        - position: the x-y position of the center of the label
        - text: a pygame surface that indicate the words and color
        - font: a pygame font that indicates the font of words and font size
        - color: rgb color of the text
        - background: the rectangular background of the label. If no background, it is None
        - visible: whether to draw visible or not
        - align: the way to align the text

    Representative Invariants:
        - self.align in ['center', 'left']
        - 0 <= self.position[0] <= WINDOW_WIDTH
        - 0 <= self.position[1] <= WINDOW_HEIGHT
    """
    position: tuple[int, int]
    text: pygame.Surface
    font: pygame.font.Font
    color: tuple[int, int, int]
    background: Optional[tuple[pygame.Rect, tuple[int, int, int]]]
    visible: bool
    align: str

    def __init__(self, position: tuple[int, int], text: str, text_style: tuple[pygame.font.Font, tuple[int, int, int]],
                 background: Optional[tuple[pygame.Rect, tuple[int, int, int]]] = None) -> None:
        """
        Initialize a label
        Preconditions:
            - all(0 <= text_style[1][i] <= 255 for i in range(3))
        """
        self.position = position
        self.font, self.color = text_style
        self.update_text(text)
        self.visible = True
        self.background = background
        self.align = 'center'

    def draw(self, surface: pygame.Surface) -> None:
        """ Draw a label on the given surface. If self.visible is False, do not draw it
        """
        if not self.visible:
            return
        if self.background is not None:
            background_rect, background_color = self.background
            pygame.draw.rect(surface, background_color, background_rect)

        if self.align == 'center':
            text_rect = self.text.get_rect(center=self.position)
            surface.blit(self.text, text_rect)
        elif self.align == 'left':
            surface.blit(self.text, self.position)

    def update_text(self, text: str) -> None:
        """
        Update the text of label
        """
        self.text = self.font.render(text, True, self.color)


def draw_circle(surface: pygame.Surface, x: int, y: int, radius: int, color: tuple[int, int, int]) -> None:
    """
    Draw an anti-aliased circle at the position (x, y) given the radius and color
    """
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def draw_rounded_rect(surface: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int], corner_radius: int) -> \
        None:
    """Draw an anti-aliased rectangle with rounded corners. We draw anti-aliased circles at the corners
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    """
    # draw four anti aliasing circles to smooth the corners
    # top left
    draw_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
    # top right
    draw_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
    # bottom left
    draw_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    # bottom right
    draw_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)
    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['__future__', 'typing', 'pygame', 'constant'],
    })
