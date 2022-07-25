def player_ships_list():
    ships_list = []
    buffer_list = []

    def buffer_zone(ship: list):
        buffer = []
        for number in ship:
            match number%10:
                case 0: buff_numbers = [ -10, -9, 1, 11, 10]
                case 9: buff_numbers = [-11, -10, 9, 10, -1]
                case _: buff_numbers = [-11, -10, -9, 1, 11, 10, 9, -1]
            for buff in buff_numbers:
                cell = buff + number
                if cell not in buffer:
                    buffer.append(cell)
        [buffer.remove(number) for number in ship if number in buffer]
        buffer_list.append(buffer)

    def error_cell(title: str, text: str):
        messagebox.showerror(title, text)
        ships_list.clear()
        return

    for ship in player_ships:
        y = int(ship.place_info().get('x'))//30 + 1
        x = int(ship.place_info().get('y'))//30 + 1
        number = 10*(x-1) + (y - 1)
        if number not in ships_list:
            temp_ship =[]
            for i in range(ship.size):
                temp_ship.append(number)
                if ship.dir() == 'hor': step = 1
                else: step = 10
                number += step
            ships_list.append(temp_ship)
            buffer_zone(temp_ship)
        if y > 9:
            error_cell('Внимание!', 'Капитан! Еще не все суда покинули верфь!')
            ships_list.clear()
            buffer_list.clear()
            return
        # else:
        #     print('Наскок', number)
        #     error_cell('Полундра!', 'Каритан! Битва еще не началась, а корабли уже врезались!')
        #     ships_list.clear()
        #     buffer_list.clear()
        #     return
    buffer = []
    [buffer.append(cell) for element in buffer_list for cell in element if cell not in buffer]

    for ship in ships_list:
        for cell in ship:
            if buffer.__contains__(cell):
                print('Рядом', cell)
                print(sorted(ships_list))
                print(sorted(buffer))
                ships_list.clear()
                buffer_list.clear()
                error_cell('Опасность!', 'Капитан! Наши корыта слишком близко! Надо расстояние хотя бы в одну клетку!')
                return

    str_player_ships_list = ''
    for ship in ships_list:
        temp_str_ship = ''
        for cell in ship:
            temp_str_ship += f'{cell} '
        str_player_ships_list += f'{temp_str_ship[:-1]}:'

    return str_player_ships_list[:-1]