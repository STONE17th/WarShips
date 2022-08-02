import tkinter as tk

global miss, water, cell, ship, fire, kill, logo_game

def init_image():
    miss = tk.PhotoImage(file="data/miss_small.png")
    water = tk.PhotoImage(file="data/water.png")
    cell = tk.PhotoImage(file="data/free_cell_water.png")
    ship_new = tk.PhotoImage(file="data/ship.png")
    fire = tk.PhotoImage(file="data/fire.png")
    kill = tk.PhotoImage(file="data/kill.png")
    logo_game = tk.PhotoImage(file="data/logo_game.png")