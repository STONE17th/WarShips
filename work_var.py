import random
import time
import tkinter as tk
import socket
from tkinter import messagebox
import net_func as nf
import ships


class Cell(tk.Button):
    def __init__(self, master, x: int, y: int, id, width, height,  *args, **kwargs):
        super(Cell, self).__init__(master, *args, **kwargs)
        self.id = id
        self.x = x
        self.y = y


    def open_cell(self):
        # global sb_client_sock
        print(self.id)
        print(self)
        match nf.send_fire(sb_client_sock, str(self.id)):
            case '0':
                self['relief'] = tk.SUNKEN
                self['image'] = miss
                print("Мимо")
            case '1':
                self['relief'] = tk.SUNKEN
                self['image'] = fire
                print("Ранил")
            case '2':
                self['relief'] = tk.SUNKEN
                self['image'] = kill
                check_kill(self.id)
                print("Убил")
            case '3':
                pass
                print("Победа")
            # CellMiss.show_hit(self.id, self.x, self.y)
            # self.cell[id]['image'] = ship_fire
            # self.cell[id].grid(row=self.x, column=self.y)
        refresh_board(cpu_cell)

        # def show_miss(id: int, x, y):
        #
        #
        # def show_hit(id: int, x, y):
        #     cell_miss[id]['image'] = ship
        #     cell_miss[id].grid(row=x, column=y)


    def __repr__(self):
        return 'Cell'


class CellLabel(tk.Label):
    def __init__(self, master, x: int, y: int, id, *args, **kwargs):
        super(CellLabel, self).__init__(master, *args, **kwargs)
        self.id = id
        self.x = x
        self.y = y

    # def show_miss(id: int, x, y):
    #     cell_miss[id]['image'] = miss
    #     cell_miss[id].grid(row=x, column=y)
    #
    # def show_hit(id: int, x, y):
    #     cell_miss[id]['image'] = ship
    #     cell_miss[id].grid(row=x, column=y)

    def __repr__(self):
        return 'CellLabel'

class Ship(tk.Canvas):
    def __init__(self, master, size, direct, image = 'pixelVirtual', *args, **kwargs):
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

def check_kill(index: int):
    pass

def refresh_board(field):
    for i in range(100):
        if str(i) in ship_player:
            field[i]['image'] = ship
        else:
            field[i]['image'] = water
        if str(i) in shoot_list:
            if str(i) in ship_player:
                field[i]['image'] = ship_fire
            else:
                field[i]['image'] = miss

def start_field(field, n):
    for x in range(10):
        for y in range(10):
            i = (y * 10) + x
            field[i].place(x = x*30 + n, y= y*30 + 10, width=30, height=30)

# def print_pos(board: list):
#     for i in range(10):
#         for j in range(10):
#             print(str(board[10*i + j]) + ' ', end='')
#         print()
#
# def shipyard(ship_count: int):
#     position = []
#     for i in range(ship_count):
#         while True:
#             num = random.randint(0, 99)
#             if num not in position:
#                 position.append(num)
#                 break
#     ship_dock = [Ship(main_window, x=x, y=y, id=(x*10 + y), width=3, height=1) for x in range(10) for y in range(10) if (x*10 + y) in position]
#     return ship_dock







main_window = tk.Tk()

ship = tk.PhotoImage(file="Data/ship.png")
ship_fire = tk.PhotoImage(file="Data/ship_fire.png")
miss = tk.PhotoImage(file="Data/miss_small.png")
water = tk.PhotoImage(file="Data/water.png")
logo = tk.PhotoImage(file="Data/logo_game.png")
cell = tk.PhotoImage(file="Data/free_cell_water.png")
ship_4 = tk.PhotoImage(file="Data/ship_4.png")
fire = tk.PhotoImage(file="Data/fire.png")
kill = tk.PhotoImage(file="Data/kill.png")
# logo_game = tk.Label(image=logo).grid(row=0,column=0,sticky='news')
# time.sleep(1)
# logo_game.destroy()

ship_cpu = [str(random.randint(0,99)) for _ in range(10)]
ship_player = [str(random.randint(0,99)) for _ in range(10)]
shoot_list = {}
player_ships = []
power_player_field = True

# board_cpu = []
# board_player = []
# player_shoot_list = []
# cpu_shoot_list = []
cpu_cell = []
my_cell = ['' for _ in range(100)]
sb_client_sock = None
player = None



def connect_to_server():
    global sb_client_sock
    sb_client_sock = nf.connect_to_host('glt.ekolenko.ru', 9091)
    if nf.check_connection(sb_client_sock):
        btn_connect['text'] = 'Disconnect'
        btn_connect['state'] = tk.DISABLED


def start_game():
    if nf.start_game(sb_client_sock):
        btn_ready['state'] = tk.DISABLED
        btn_ready['text'] = 'хуй'
        start_field(cpu_cell, 10)

def find_player():
    btn_find['text'] = nf.find_player(sb_client_sock)


def send_player_field():
    player_field = player_ships_list()
    print(player_field)
    start_field(my_cell, 360)
    if nf.send_field(sb_client_sock, player_field):
        btn_send['state'] = tk.DISABLED
        btn_send['text'] = 'OK'
        disable_player_ships()
        disable_player_field(cpu_cell)

def disable_player_ships():
    for ship in player_ships:
        ship.unbind('<B1-Motion>')
        ship.unbind('<Button-3>')

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

def on_closing():
    if messagebox.askyesno("Уходите?", "Вы хотите на покинуть?"):
        if sb_client_sock != None:
            nf.disconnect_sock(sb_client_sock)
        main_window.destroy()

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


main_window.iconphoto(False, ship)
main_window.protocol('WM_DELETE_WINDOW', on_closing)
main_window.title("Убийца WarShips")
main_window.geometry('670x360+900+400')
main_window.resizable(False,False)
main_window.wm_attributes("-topmost", 1)


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

# battle_field = tk.Canvas(main_window, width=300, height=300, bg='GREEN')
# battle_field.create_rectangle(10,10, 40, 130, fill='WHITE')
# battle_field.place(x=10, y=10)

# cell_player = [Cell(main_window, x=x, y=y, id=(x*10 + y), width=3, height=1) for x in range(10) for y in range(10)]
# for i in range(100):
#     cell_player[i]['command'] = cell_player[i].open_cell
cpu_cell = [Cell(main_window, x=x, y=y, id=(x * 10 + y), width=3, height=1, image=cell) for x in range(10) for y in range(10)]
my_cell = [Cell(main_window, x=x, y=y, id=(x*10 + y), width=25, height= 10, image=water) for x in range(10) for y in range(10)]
for i in range(100):
    my_cell[i]['command'] = my_cell[i].open_cell
refresh_board(my_cell)
# cell_miss = [CellMiss(main_window, x=x, y=y, id=(x*10 + y), image=miss) for x in range(10) for y in range(10)]
enemy_cell=[CellLabel(main_window, x=0, y=0, id=(x*10 + y)) for x in range(10) for y in range(10)]
btn_connect = tk.Button(main_window, text='Connect', command= connect_to_server)
btn_send = tk.Button(main_window, text='Send', command=send_player_field)
btn_ready = tk.Button(main_window, text='Ready', command=start_game)
btn_find = tk.Button(main_window, text='Find', command=find_player)

start_field(cpu_cell, 10)



s = 4
while s:
    for j in range (s):
        player_ships.append(Ship(main_window, width=30, height=30*s, size = 4-s+1, direct = 'ver',  bg = 'GRAY'))
    s = s - 1


player_ships[0].place(x=360, y=10, width=30, height=30)
player_ships[1].place(x=420, y=10, width=30, height=30)
player_ships[2].place(x=480, y=10, width=30, height=30)
player_ships[3].place(x=540, y=10, width=30, height=30)
player_ships[4].place(x=360, y=70, width=30, height=60)
player_ships[5].place(x=420, y=70, width=30, height=60)
player_ships[6].place(x=480, y=70, width=30, height=60)
player_ships[7].place(x=360, y=160, width=30, height=90)
player_ships[8].place(x=420, y=160, width=30, height=90)
player_ships[9].place(x=540, y=130, width=30, height=120)


for ship in player_ships:
    ship.bind('<B1-Motion>', ship_drag)
    ship.bind('<Button-3>', ship_rotate)



btn_send.place(x=40 , y=320 , width=90, height = 30)
btn_find.place(x= 190, y=320, width=90, height = 30)
btn_connect.place(x=500 , y=320 , width=90, height = 30)
btn_ready.place(x= 390, y=320, width=90, height = 30)


# [main_window.grid_columnconfigure(i, minsize= 24, pad= 0) for i in range(22)]
# [main_window.grid_rowconfigure(i, minsize=4, pad=0) for i in range(12)]

main_window.mainloop()