"""
Provides Tkinter-based visualization capabilities.
"""

import tkinter

from vis2048.game import Game
from vis2048.vec2 import Vec2

BG_COLOR_GAME = "#92877d"

BG_COLOR_TILE = {
    None: "#9e948a",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}

FG_COLOR_DICT = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2"
}

FG_COLOR_MSG = 'black'
BG_COLOR_MSG = 'white'

KEY_UP = "<Up>"
KEY_DOWN = "<Down>"
KEY_LEFT = "<Left>"
KEY_RIGHT = "<Right>"


class GameVis(tkinter.Frame):
    """
    A visualization as a Tkinter component.
    """

    def __init__(self, game=None, grid_padding=5,
                 font_size=40, font_name='Verdana', font_style='bold', **kwargs):
        """
        :param game: A game to use, otherwise a standard game will be created.
        :param grid_padding: The padding of the grid.
        :param font_size: The size of the font.
        :param font_name: The name of the font.
        :param font_style: Special style for font.
        :param kwargs: Arguments passed on the the  tkinter.Frame constructor.
        """
        tkinter.Frame.__init__(self, **kwargs)

        self.grid_padding = grid_padding
        self.font = (font_name, font_size, font_style)
        self.game = game or Game(4, 2, 2048)

        self.game.place_two()
        self.game.place_two()

        self.grid_cells = []

        self._init_vis()
        self.update_vis()

    def update_vis(self):
        """
        Update the visualization. Should be called whenever the game itself is mutated.
        """
        for i in range(self.game.width):
            for j in range(self.game.width):
                new_number = self.game.mat[Vec2(j, i)]
                if new_number is None:
                    self.grid_cells[i][j].configure(text="", bg=BG_COLOR_TILE[None])
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BG_COLOR_TILE[new_number],
                                                    fg=FG_COLOR_DICT[new_number])

        if self.game.won():
            self._show_msg('You Win!')
        elif self.game.stuck():
            self._show_msg('You Lose!')

        self.update_idletasks()
        self.update()

    def _show_msg(self, msg):
        msg_lbl = tkinter.Label(master=self, fg=FG_COLOR_MSG, bg=BG_COLOR_MSG, text=msg, font=self.font)
        msg_lbl.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

    def _init_vis(self):
        width = self.game.width

        background = tkinter.Frame(self, bg=BG_COLOR_GAME)
        background.grid()
        for i in range(width):
            grid_row = []
            for j in range(width):
                cell = tkinter.Frame(background, bg=BG_COLOR_TILE[None])
                cell.grid(row=i, column=j, padx=self.grid_padding, pady=self.grid_padding)
                t = tkinter.Label(cell, text="", bg=BG_COLOR_TILE[None], justify=tkinter.CENTER,
                                  font=self.font, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)


class GameVisDemo(tkinter.Frame):
    """
    A visualization demonstration packaged as a Tkinter frame.
    """

    def __init__(self):
        tkinter.Frame.__init__(self)

        self.all_gamevis = []

        self.grid()
        self.master.title('vis2048 - Demo with 4 simultaneous games')
        self.master.bind("<Up>", self._key_down(self._up))
        self.master.bind("<Down>", self._key_down(self._down))
        self.master.bind("<Left>", self._key_down(self._left))
        self.master.bind("<Right>", self._key_down(self._right))

        background = tkinter.Frame()
        background.grid()

        for i in range(4):
            gamevis = GameVis(master=background, font_size=20)
            gamevis.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.all_gamevis.append(gamevis)

            if i == 0:
                gamevis.game.mat[Vec2(0, 0)] = 1024
                gamevis.game.mat[Vec2(0, 1)] = 1024
                gamevis.update_vis()

    def _key_down(self, func):
        # noinspection PyUnusedLocal
        def handler(event):
            for gamevis in self.all_gamevis:
                if gamevis.game.won() or gamevis.game.stuck():
                    continue
                func(gamevis)

                if not gamevis.game.full():
                    gamevis.game.place_two()

                gamevis.update_vis()

        return handler

    def _up(self, gamevis):
        gamevis.game.up()

    def _down(self, gamevis):
        gamevis.game.down()

    def _left(self, gamevis):
        gamevis.game.left()

    def _right(self, gamevis):
        gamevis.game.right()
