import tkinter as tk
from tkinter import messagebox
import net_func as nf

# ============================= КЛАССЫ ================================================================================

class Cell(tk.Button):
    def __init__(self, master, x: int, y: int, id, *args, **kwargs):
        super(Cell, self).__init__(master, *args, **kwargs)
        self.id = id
        self.x = x
        self.y = y

    def open_cell(self):
        print(self.id)
        match nf.send_fire(sb_client_sock, str(self.id)):
            case '0':
                self['image'] = miss
                self['relief'] = tk.SUNKEN
            case '1':
                self['image'] = fire
                self['relief'] = tk.SUNKEN
            case '2':
                self['image'] = kill
                self['relief'] = tk.SUNKEN
            case '3':
                pass
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
        shipyard()
        start_field(my_field, 10)
        btn_connect['text'] = 'Disconnect'
        btn_connect['state'] = tk.DISABLED

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
        case '1':
            print(qwerty)
            btn_find['text'] = 'Ход врага'
        case _:
            print(qwerty)
            btn_find['text'] = 'Не найден'

def send_player_field():
    player_field = player_ships_list()
    print(player_field)
    start_field(my_field, 10)
    start_field(enemy_field, 360)
    if nf.send_field(sb_client_sock, player_field):
        btn_send['state'] = tk.DISABLED
        btn_send['text'] = 'OK'
        disable_player_ships()
        disable_player_field(my_field)

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


# ============================= КОРАБЛИ ===============================================================================


def check_kill(index: int):
    pass

def shipyard():
    s = 4
    while s:
        for j in range(s):
            player_ships.append(Ship(main_window, width=30, height=30 * s, size=4 - s + 1, direct='ver', bg='GRAY'))
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
ship = tk.PhotoImage(file="Data/kill.png")

# ============================= ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ========================================

my_field = []
enemy_field = []
shoot_list = {}
player_ships = []
power_player_field = True
# cpu_cell = []
# my_cell = ['' for _ in range(100)]
sb_client_sock = None
player = None

# ============================= ИГРОВЫЕ ПОЛЯ ========================================


[my_field.append(Cell(main_window, x=x, y=y, id=(x * 10 + y), width=3, height=1, image=cell)) for x in range(10) for y in range(10)]
[enemy_field.append(Cell(main_window, x=x, y=y, id=(x*10 + y), width=25, height= 10, image=water)) for x in range(10) for y in range(10)]
for i in range(100):
    enemy_field[i]['command'] = enemy_field[i].open_cell

# ======================================== ПРИВЯЗКА КНОПОК =================================

btn_connect = tk.Button(main_window, text='Connect', command= connect_to_server)
btn_send = tk.Button(main_window, text='Send', command=send_player_field)
btn_ready = tk.Button(main_window, text='Ready', command=start_game)
btn_find = tk.Button(main_window, text='Find', command=find_player)

btn_send.place(x=40 , y=320 , width=90, height = 30)
btn_find.place(x= 190, y=320, width=90, height = 30)
btn_connect.place(x=540 , y=320 , width=90, height = 30)
btn_ready.place(x= 390, y=320, width=90, height = 30)

main_window.mainloop()