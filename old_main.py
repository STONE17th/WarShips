import random
import tkinter as tk
from tkinter import messagebox
import net_func as nf

# ============================= КЛАССЫ ================================================================================

class Game:

    def __init__(self, enemy_round,listen_sock):
        self.enemy_round = enemy_round
        self.listen_sock = listen_sock

class Cell(tk.Button):
    def __init__(self, master, x: int, y: int, cell, *args, **kwargs):
        super(Cell, self).__init__(master, *args, **kwargs)
        self.cell = []
        self.x = x
        self.y = y

    def open_cell(self):
        print(self.id)
        print(game.enemy_round)
        if game.enemy_round:
            return
        match nf.send_fire(sb_client_sock, str(self.id)):
            case '0':
                my_shoot_list[self.id] = False
                self['image'] = miss
                self['relief'] = tk.SUNKEN
                game.enemy_round = True
                nf.receive_fire(sb_client_sock, btn_find, game)

            case '1':
                my_shoot_list[self.id] = True
                self['image'] = fire
                self['relief'] = tk.SUNKEN
            case '2':
                my_shoot_list[self.id] = True
                self['image'] = kill
                self['relief'] = tk.SUNKEN
                check_kill(self.id)
            case '3':
                messagebox.INFO('Победа!', 'Капитан, поздравляем! Мы надрали им зад!')
                print("Победа")

    def __repr__(self):
        return 'Cell'


class Ship(tk.Canvas):
    def __init__(self, master, size, direct, *args, **kwargs):
        super(Ship, self).__init__(master, *args, **kwargs)
        self.size = size
        self.direct = direct

    def dir(self):
        return self.direct

    def change_dir(self):
        if self.direct == 'hor':
            self.direct = 'ver'
        else: self.direct = 'hor'

    def size(self):
        return self.size

    def __repr__(self):
        return 'Ship'


def on_closing():
    if messagebox.askyesno("Уходите?", "Вы хотите на покинуть?"):
        if sb_client_sock != None:
            nf.disconnect_sock(sb_client_sock)
        main_window.destroy()

# ============================= ФУНКЦИИ СЕРВЕРА =======================================================================

def connect_to_server():
    global sb_client_sock
    sb_client_sock = nf.connect_to_host('glt.ekolenko.ru', 9091)
    if nf.check_connection(sb_client_sock):
        shipyard(player_ships)
        start_field(my_cell, 10)
        btn_connect['text'] = 'Disconnect'
        btn_connect['state'] = tk.DISABLED
        btn_random.place(x=360, y=270, width=300, height=30)


def start_game():
    if nf.start_game(sb_client_sock):
        btn_ready['state'] = tk.DISABLED
        btn_ready['text'] = 'хуй'

def find_player():

    qwerty = nf.find_player(sb_client_sock)
    match qwerty:
        case '0':
            print(qwerty)
            btn_find['text'] = 'Твой ход'
            game.enemy_round = False
        case '1':
            game.enemy_round = True
            print(qwerty)
            btn_find['text'] = 'Ход врага'
            nf.receive_fire(sb_client_sock, btn_find, game)
        case _:
            print(qwerty)
            btn_find['text'] = 'Не найден'

def send_player_field():
    player_field = player_ships_list(player_ships)
    print(player_field)
    start_field(my_cell, 10)
    start_field(enemy_cell, 360)
    # ship_arrangement_done()
    if nf.send_field(sb_client_sock, player_field):
        btn_send['state'] = tk.DISABLED
        btn_send['text'] = 'OK'
        disable_player_ships()
        disable_player_field(my_cell)
        btn_random.destroy()

# ============================= ФУНКЦИИ ИГРЫ ==========================================================================

def start_field(field: Ship, n):
    for x in range(10):
        for y in range(10):
            i = (y * 10) + x
            field[i].place(x = x*30 + n, y= y*30 + 10, width=30, height=30)

def disable_player_field(field):
    global power_player_field
    if power_player_field:
        for cell in field:
            cell['state'] = tk.DISABLED
            power_player_field = False
    else:
        for cell in field:
            cell['state'] = tk.NORMAL
            power_player_field = True

# def ship_arrangement_done():
#     numbers = []
#     for ship in player_ships_list().split(':'):
#         for cell in ship:
#             numbers.append(cell)
#
#     for num in numbers:
#         my_cell[int(num)]['image'] = ship
#     for ship in player_ships:
#         print(ship)
#         ship.destroy()

# ============================= КОРАБЛИ ===============================================================================

def check_kill(index: int):
    destroyed_ship = []
    print(my_shoot_list)
    for k in [1, 10]:
        new_index = index + k
        if new_index >= 0 or new_index < 100:
            if my_shoot_list[index + k] == True or my_shoot_list[index - k] == True:
                for i in range(-3, 3):
                    ind = index + i*k
                    if ind >= 0 or ind < 100:
                        if my_shoot_list[ind] == True:
                            enemy_cell[ind]['image'] = kill
                            destroyed_ship.append(ind)
                    else: pass
        else: pass
                # alt_index = (sorted(destroyed_ship))[0] - k

            # if k == 10: n = 1
            # else: n = 10
            # for l in range(len(destroyed_ship) + 2):
            #     for j in range(-n, n+1, n):
            #         if my_shoot_list[alt_index + j] == None: my_shoot_list[alt_index + j] = False
            #         enemy_cell[alt_index + j]['relief'] = tk.SUNKEN
            #         enemy_cell[alt_index + j]['image'] = miss
            #     alt_index += k
            # for cell in destroyed_ship:
            #     enemy_cell[cell]['image'] = kill
            # print(my_shoot_list)
            # print(destroyed_ship)


def shipyard(player_ships: list):
    s = 4
    n = 0
    while s:
        for i in range(s):
            k = 5 - s
            player_ships.append(Ship(game_window, x=0 , y=0, width=30, height=30 * s, size=k, direct='ver', bg='GRAY'))
            player_ships[n].place(x=10 + 30 * (i*player_ships[n].size), y=10 + 30*(4-s), width=player_ships[n].size * 30, height=30)

            print(player_ships[n].size)
            n += 1
        s = s - 1

    for ship in player_ships:
        ship.bind('<B1-Motion>', ship_drag)
        ship.bind('<Button-3>', ship_rotate)

def disable_player_ships():
    for ship in player_ships:
        ship.unbind('<B1-Motion>')
        ship.unbind('<Button-3>')

def ship_drag(event):
    mouse_x = main_window.winfo_pointerx() - main_window.winfo_rootx()
    mouse_y = main_window.winfo_pointery() - main_window.winfo_rooty()
    event.widget.place(x=mouse_x-10, y=mouse_y-10)
    ship_x = event.widget.place_info().get('x')
    ship_y = event.widget.place_info().get('y')
    ship_x = ((int(ship_x) + 10) // 30) * 30 + 10
    ship_y = ((int(ship_y) + 10) // 30) * 30 + 10
    event.widget.place(x=ship_x, y=ship_y)

def ship_rotate(event):
    event.widget.change_dir()
    wid_w = event.widget.place_info().get('width')
    wid_h = event.widget.place_info().get('height')
    event.widget.place(width= wid_h)
    event.widget.place(height= wid_w)

def ship_rotate_random(ship):
    ship.change_dir()
    wid_w = ship.place_info().get('width')
    wid_h = ship.place_info().get('height')
    ship.place(width= wid_h)
    ship.place(height= wid_w)

def player_ships_list(player_ships):
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
        print(x, y)
        if number not in ships_list:
            temp_ship =[]
            for i in range(ship.size):
                temp_ship.append(number)
                if ship.dir() == 'hor': step = 1
                else: step = 10
                number += step
            ships_list.append(temp_ship)
            buffer_zone(temp_ship)
        if x > 11:
            error_cell('Внимание!', 'Капитан! Еще не все суда покинули верфь!')
            ships_list.clear()
            buffer_list.clear()
            return
        # else:
        #     print('Наскок', number)
        #     error_cell('Полундра!', 'Капитан! Битва еще не началась, а корабли уже врезались!')
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

def random_ships():
    while player_ships_random():
        pass

def player_ships_random():
    for ship in player_ships:
        while True:
            size_of_ship = ship.size
            direct = random.randint(0,1)
            x = random.randint(0, 9)*30 +10
            y = random.randint(0, (10 - size_of_ship))*30 + 10
            if direct == 0:
                ship_rotate_random(ship)
                ship.place(x=y, y=x)
                ship_lenght = x + size_of_ship*30
            else:
                ship.place(x=x, y=y)
                ship_lenght = y + size_of_ship * 30
            if ship_lenght < 320: break

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

    for ship in player_ships:
        y = int(ship.place_info().get('x'))//30 + 1
        x = int(ship.place_info().get('y'))//30 + 1
        number = 10*(x-1) + (y - 1)
        if number not in ships_list:
            temp_ship =[]
            for i in range(ship.size):
                ships_list.append(number)
                temp_ship.append(number)
                if ship.dir() == 'hor': step = 1
                else: step = 10
                number += step
            buffer_zone(temp_ship)
        else:
            ships_list.clear()
            buffer_list.clear()
            return True
    buffer = []
    [buffer.append(cell) for element in buffer_list for cell in element if cell not in buffer]

    for cell in ships_list:
            if buffer.__contains__(cell):
                ships_list.clear()
                buffer_list.clear()
                return True
    return False

# ============================= НАСТРОЙКИ ОКНА ========================================

main_window = tk.Tk()
main_window.protocol('WM_DELETE_WINDOW', on_closing)
main_window.title("Убийца WarShips")
main_window.geometry('670x360+900+400')
main_window.resizable(False,False)
main_window.wm_attributes("-topmost", 1)


# ============================= ГРАФИКА ========================================

miss = tk.PhotoImage(file="Data/miss_small.png")
water = tk.PhotoImage(file="Data/water.png")
cell = tk.PhotoImage(file="Data/free_cell_water.png")
fire = tk.PhotoImage(file="Data/fire.png")
kill = tk.PhotoImage(file="Data/kill.png")
ship = tk.PhotoImage(file="Data/ship.png")
logo = tk.PhotoImage(file="Data/logo_game.png")

# ============================= ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ========================================

my_cell = []
enemy_cell = []
my_shoot_list = {}
for i in range(100):
    my_shoot_list[i] = None
enemy_shoot_list = {}
for i in range(100):
    my_shoot_list[i] = None
player_ships = []
power_player_field = True
sb_client_sock = None
player = None
game = Game(False,False)

# ============================= ИГРОВЫЕ ПОЛЯ ========================================

def create_board (board: list):
    ind = 1
    for i in range(12):
        for j in range(12):
            if i == 0 or j == 0 or i == 11 or j == 11:
                board.append(Ship(main_window, direct=0, size=0, x=0, y=0))
            else:
                id = int(str(i - 1) + str(j))
                board.append(Ship(main_window, direct=ind, size=0, x=i, y=j))
                ind += 1

[enemy_cell.append(Cell(main_window, x=x, y=y, id=(x * 10 + y), width=25, height= 10, image=water)) for x in range(10) for y in range(10)]
for i in range(100):
    enemy_cell[i]['command'] = enemy_cell[i].open_cell

# ======================================== ПРИВЯЗКА КНОПОК =================================

btn_connect = tk.Button(main_window, text='Connect', command= connect_to_server)
btn_send = tk.Button(main_window, text='Send', command=send_player_field)
btn_ready = tk.Button(main_window, text='Ready', command=start_game)
btn_find = tk.Button(main_window, text='Find', command=find_player)
btn_random = tk.Button(main_window, text='Random', command=random_ships)

btn_send.place(x=40 , y=320 , width=90, height = 30)
btn_find.place(x= 190, y=320, width=90, height = 30)
btn_connect.place(x=540 , y=320 , width=90, height = 30)
btn_ready.place(x= 390, y=320, width=90, height = 30)

main_window.mainloop()