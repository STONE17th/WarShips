for k, v in cell_xy.items():
    if v == (x, y):
        cur_position = k
if cur_position not in ships_position:
    ships_position.append(cur_position)
    ship.x = x + 1
    ship.y = y + 1
    ship.place(x=x * 30 + 10, y=y * 30 + 10)