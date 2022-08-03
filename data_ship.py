import random
from tkinter import messagebox


def create_dictionary():
    dict = {}
    index = 1
    for i in range(1,11):
        for j in range(1,11):
            dict[index] = (i,j)
            index += 1
    return dict

def random_ship_position(player_ships):
    ships_position = []
    buffer_position = []
    counter = 0

    def create_ship(ship):
        if random.randint(0, 1):
            ship_rotate_random(ship)
        ship.x = random.randint(1, 10)
        ship.y = random.randint(1, 10)
        for cell in ship.cell_ship():
            if not 0<cell<101:
                return False
        return True

    for ship in player_ships:
        while True:
            if counter > 10000: break
            if create_ship(ship):
                temp_ship = ship.cell_ship()
                temp_buffer = ship.cell_buffer()
                if comparison(temp_ship, ships_position):
                    if comparison(temp_ship, buffer_position):
                        [ships_position.append(temp) for temp in temp_ship]
                        [buffer_position.append(temp) for temp in temp_buffer if not temp in buffer_position]
                        ship.place(x=(ship.x-1) * 30 + 10, y=(ship.y - 1) * 30 + 10)
                        break
            counter += 1


def comparison(ship, list):
        for cell in ship:
            if cell in list:
                return False
        else: return True

def xy_to_id(ship):
    k = [k for k, v in dict_id.items() if v == (ship.y, ship.x)]
    if not k == []: return int(k[0])
    else: return 0

def ship_rotate_random(ship):
    ship.change_dir()
    wid_w = ship.place_info().get('width')
    wid_h = ship.place_info().get('height')
    ship.place(width= wid_h)
    ship.place(height= wid_w)

def out_of_shipyard(ship_position):
    for ship in ship_position:
        if ship.direct:
            if ship.x > 11 or ship.y + ship.size > 11:
                print(ship.x, ship.y, ship.size)
                messagebox.showinfo('Капитан!', 'Капитан, мы не можем отправить расположение кораблей! Не все корабли в зоне действий!')
                return False
        else:
            if ship.x + ship.size > 11 or ship.y > 11:
                print(ship.x, ship.y, ship.size)
                messagebox.showinfo('Капитан!', 'Капитан, мы не можем отправить расположение кораблей! Не все корабли в зоне действий!')
                return False
    return True

def ship_collision(list, message):
    buffer_zone = []
    for ship in list:
        for cell in ship.cell_buffer():
            if not cell in buffer_zone: buffer_zone.append(cell)
    for ship in list:
        for cell in ship.cell_ship():
            if cell in buffer_zone:
                if message:
                    ship['bg'] = 'RED'
                    messagebox.showinfo('Капитан!', 'Капитан, бой еще не начался, а мы уже врезались! Расставьте корабли на расстоянии хотя бы ОДНОЙ клетки!')
                return True
    return False

def ship_overlay(list, message):
    for ship_on_water in list:
        for ship in list:
            for cell in ship.cell_ship():
                if cell in ship_on_water.cell_ship() and not ship.id == ship_on_water.id:
                    if message:
                        ship_on_water['bg'] = 'RED'
                        ship['bg'] = 'RED'
                        messagebox.showinfo('Капитан!', 'Капитан, не мне вас учить, но корабль не может быть в КОРАБЛЕ! Поставьте рядышком, что ли...')
                    return True
    return False



dict_id = create_dictionary()