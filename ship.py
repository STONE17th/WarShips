import random


def random_ship_position(player_ships, id_dict):

    ships_position = []
    ships_position.clear()
    buffer_position = []
    buffer_position.clear()
    id_dic = id_dict
    counter = 0

    def xy_to_id(ship):
        k = [k for k, v in id_dic.items() if v == (ship.y, ship.x)]
        if not k == []: return int(k[0])
        else: return 0

    def cell_ship(ship):
        temp_ship = []
        x, y = ship.x, ship.y
        if ship.size == 1:
            temp_ship.append(int(xy_to_id(ship)))
            ship.x, ship.y = x, y
            return temp_ship
        else:
            for i in range(ship.size):
                temp_ship.append(xy_to_id(ship))
                if ship.direct:
                    ship.y += 1
                else:
                    ship.x += 1
            ship.x, ship.y = x, y
            return temp_ship

    def cell_buffer(ship):
        temp_buffer = []
        buffer = [-1, 0, 1]
        x, y = ship.x, ship.y
        if ship.size == 1:
            for i in buffer:
                for j in buffer:
                    temp_x, temp_y = ship.x, ship.y
                    ship.x += i
                    ship.y += j
                    temp_buffer.append(xy_to_id(ship))
                    ship.x, ship.y = temp_x, temp_y
        else:
            for i in range(ship.size):
                for i in buffer:
                    for j in buffer:
                        temp_x, temp_y = ship.x, ship.y
                        ship.x += i
                        ship.y += j
                        temp_buffer.append(xy_to_id(ship))
                        ship.x, ship.y = temp_x, temp_y
                if ship.direct:
                    ship.y += 1
                else:
                    ship.x += 1
        for cell in temp_ship:
            if cell in temp_buffer: temp_buffer.remove(cell)
        ship.x, ship.y = x, y
        return set(temp_buffer)

    def create_ship(ship):
        if random.randint(0, 1):
            ship_rotate_random(ship)
        ship.x = random.randint(1, 11)
        ship.y = random.randint(1, 11)
        if ship.size + ship.x < 12 and ship.size + ship.y < 12:
            return True

    def comparison(ship, list):
        for cell in ship:
            if cell in list:
                return False
        else: return True

    for ship in player_ships:
        while True:
            if counter > 10000: break
            if create_ship(ship):
                temp_ship = cell_ship(ship)
                temp_buffer = cell_buffer(ship)
                if comparison(temp_ship, ships_position):
                    if comparison(temp_ship, buffer_position):
                        [ships_position.append(temp) for temp in temp_ship]
                        [buffer_position.append(temp) for temp in temp_buffer if not temp in buffer_position]
                        ship.place(x=(ship.x-1) * 30 + 10, y=(ship.y - 1) * 30 + 10)
                        break
            counter += 1
    if len(ships_position) == 20: return ships_position
    else: random_ship_position(player_ships, id_dic)


def ship_rotate_random(ship):
    ship.change_dir()
    wid_w = ship.place_info().get('width')
    wid_h = ship.place_info().get('height')
    ship.place(width= wid_h)
    ship.place(height= wid_w)