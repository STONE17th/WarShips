import data_ship
import tkinter as tk
import net_func as nf
from tkinter import messagebox


class Game:
    def __init__(self, enemy_round,listen_sock):
        self.enemy_round = enemy_round
        self.listen_sock = listen_sock
        self.id = 0
        self.enemy_shoot_list = []

class Cell(tk.Button):
    def __init__(self, master, x: int, y: int, id, *args, **kwargs):
        super(Cell, self).__init__(master, *args, **kwargs)
        self.id = id
        self.x = x
        self.y = y

    def open_cell(self):
        if game.enemy_round:
            return
        my_shoot = nf.send_fire(sb_client_sock, game.id, (self.x, self.y))
        match my_shoot[0]:
            case 0:
                self['image'] = miss
                self['relief'] = tk.SUNKEN
                game.enemy_round = True
                nf.receive_fire(sb_client_sock, btn_connect, game, my_cell)
            case 1:
                self['image'] = fire
                self['relief'] = tk.SUNKEN
            case 2:
                self['image'] = kill
                self['relief'] = tk.SUNKEN
                check_kill(my_shoot[1], my_shoot[2], my_shoot[3], my_shoot[4], enemy_cell)
            case 3:
                messagebox.showinfo('Победа!', 'Капитан, поздравляем! Мы надрали им зад!')
            case _:
                pass

    def shoot_cell(self):
        for ship in player_ships:
            for ship_cell in ship.cell_ship():
                if self.id == ship.cell:
                    self['image'] = fire
                else:
                    self['image'] = miss

    def __repr__(self):
        return 'Cell'


class Ship(tk.Canvas):
    def __init__(self, master, id, x, y, size, direct, *args, **kwargs):
        super(Ship, self).__init__(master, *args, **kwargs)
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.direct = direct
        self.cells = self.cell_ship()
        self.buffer = self.cell_buffer()

    def change_dir(self):
        if self.direct == 1:
            self.direct = 0
        else: self.direct = 1

    def cell_ship(self):
        temp_ship = []
        x, y = self.x, self.y
        if self.size == 1:
            cell = xy_to_id(y, x, create_dictionary())
            temp_ship.append(cell)
        else:
            for i in range(self.size):
                cell = xy_to_id(y, x, create_dictionary())
                temp_ship.append(cell)
                if self.direct:
                    y += 1
                else:
                    x += 1
        return sorted(temp_ship)

    def cell_buffer(self):
        temp_buffer = []
        buffer = [-1, 0, 1]
        x, y = self.x, self.y
        for i in range(self.size):
            for i in buffer:
                for j in buffer:
                    t_x, t_y = x, y
                    t_x += i
                    t_y += j
                    cell = xy_to_id(t_y, t_x, create_dictionary())
                    if not cell in temp_buffer: temp_buffer.append(cell)
            if self.direct:
                y += 1
            else:
                x += 1
        for cell in Ship.cell_ship(self):
            if cell in temp_buffer: temp_buffer.remove(cell)
        return sorted(temp_buffer)



    def __repr__(self):
        return f'Ship ({self.x},{self.y}), size {self.size}, direct {self.direct}'


def on_closing():
    if messagebox.askyesno("Уходите?", "Вы хотите нас покинуть?"):
        if sb_client_sock != None:
            nf.disconnect_sock(sb_client_sock, game.id)
        main_window.destroy()

def connect_btn():
    global sb_client_sock, player_ships
    sb_client_sock = nf.connect_to_host('glt.ekolenko.ru', 9091)
    if nf.check_connection(sb_client_sock):
        place_field(my_cell, 0)
        player_ships = shipyard()
        btn_random.place(x=370, y=280, width=300, height=30)
        logo_game.destroy()
        btn_connect['command'] = ready_btn
        btn_connect['text'] = 'Ready?'

def send_btn():
    if data_ship.out_of_shipyard(player_ships):
        if not data_ship.ship_overlay(player_ships, True):
            if not data_ship.ship_collision(player_ships, True):
                for ship in player_ships:
                    ship['bg'] = 'GREY'
                btn_random.destroy()
                place_field(enemy_cell, 1)
                send_ship_position(player_ships)
                draw_ships(player_ships, my_cell)
                my_ships = []
                for ship in player_ships:
                    my_ships.append((ship.size, ship.direct, ship.x, ship.y))
                if nf.send_field(sb_client_sock, my_ships):
                    btn_connect['command'] = find_btn
                    btn_connect['text'] = 'Найти соперника'

def ready_btn():
    if nf.start_game(sb_client_sock):
        btn_connect['command'] = send_btn
        btn_connect['text'] = 'Send Field'

def find_btn():
    if game.id == 0:
        nf.find_player(sb_client_sock, btn_connect, game, my_cell)
    else:
        nf.receive_fire(sb_client_sock, btn_connect, game, my_cell)
    btn_connect['state'] = tk.DISABLED

def random_btn():
    global ships_position
    ships_position = data_ship.random_ship_position(player_ships)


def create_dictionary():
    dict = {}
    index = 1
    for i in range(1,11):
        for j in range(1,11):
            dict[index] = (i,j)
            index += 1
    return dict


def create_board (board: list, image: any):
    ind = 1
    for i in range(12):
        for j in range(12):
            if i == 0 or j == 0 or i == 11 or j == 11: board.append(Cell(main_window, id=0, x=0, y=0))
            else:
                board.append(Cell(main_window, id=ind, x=i, y=j, image=image))
                ind += 1
    return board

def place_field(field, n):
    index = 1
    for i in range(144):
        if not field[i].id == 0:
            dict_cell_id[index] = i
            cell_xy[i] = (field[i].x, field[i].y)
            x = 10 + (field[i].x- 1)*30 + n*360
            y = 10 + (field[i].y -1)*30
            field[i].place(x=x, y=y, width=30, height=30)
            field[i]['command'] = field[i].open_cell
            index += 1
    return cell_xy

def draw_ships(player_ships, board):
    for cell_board in board:
        for ship in player_ships:
            for cell_ship in ship.cell_ship():
                if cell_board.id == cell_ship:
                    cell_board['image'] = player_ship
    for ship in player_ships:
        ship.place_forget()

def shipyard():
    player_ships = []
    s = 4
    index = 0
    space_y = 0
    while s:
        space_x = 0
        for i in range(s):
            k = 5 - s
            player_ships.append(Ship(main_window, id=index+1, x=0 , y=0, width=30, height=30 * s, size=k, direct=0, bg='GRAY'))
            player_ships[index].place(x=370 + 30 * (i*player_ships[index].size)+space_x, y=10 + 30*(4-s) + space_y, width=player_ships[index].size * 30, height=30)
            space_x += 30
            index += 1
        space_y += 30
        s = s - 1
    for ship in player_ships:
        ship.bind('<B1-Motion>', ship_drag)
        ship.bind('<Button-3>', ship_rotate)
    return player_ships

def ship_drag(event):
    event.widget['bg'] = 'GREY'
    mouse_x = main_window.winfo_pointerx() - main_window.winfo_rootx()
    mouse_y = main_window.winfo_pointery() - main_window.winfo_rooty()
    event.widget.place(x=mouse_x-10, y=mouse_y-10)
    ship_x = event.widget.place_info().get('x')
    ship_y = event.widget.place_info().get('y')
    ship_x = ((int(ship_x) + 10) // 30) * 30 + 10
    ship_y = ((int(ship_y) + 10) // 30) * 30 + 10
    event.widget.place(x=ship_x, y=ship_y)
    event.widget.x = int((ship_x-10)/30 + 1)
    event.widget.y = int((ship_y-10)/30 + 1)

def ship_rotate(event):
    event.widget.change_dir()
    wid_w = event.widget.place_info().get('width')
    wid_h = event.widget.place_info().get('height')
    event.widget.place(width= wid_h)
    event.widget.place(height= wid_w)

def send_ship_position(player_ships):
    for ship in player_ships:
        ship_x = ship.place_info().get('x')
        ship_y = ship.place_info().get('y')
        ship_x = ((int(ship_x) + 10) // 30) * 30 + 10
        ship_y = ((int(ship_y) + 10) // 30) * 30 + 10
        ship.x = int((ship_x - 10) / 30 + 1)
        ship.y = int((ship_y - 10) / 30 + 1)

def xy_to_id(x, y, dictionary):
    k = [k for k, v in dictionary.items() if v == (y, x)]
    if k == []: return 0
    else: return int(k[0])

def check_kill(size, direct, x, y, enemy_board):
    ship = Ship(main_window, id=0, x=0, y=0, size=0, direct=0)
    ship.size, ship.direct, ship.x, ship.y = size, direct, x, y
    for index in ship.cell_buffer():
        if not dict_cell_id.get(index) == None:
            enemy_board[dict_cell_id.get(index)]['relief'] = tk.SUNKEN
            enemy_board[dict_cell_id.get(index)]['image'] = miss
    for index in ship.cell_ship():
        if not dict_cell_id.get(index) == None:
            enemy_board[dict_cell_id.get(index)]['relief'] = tk.SUNKEN
            enemy_board[dict_cell_id.get(index)]['image'] = kill



my_cell = []
enemy_cell = []
player_ships = []

cell_xy = {}
dict_cell_id = {}
game = Game(False,False)

sb_client_sock = None

main_window = tk.Tk()
main_window.protocol('WM_DELETE_WINDOW', on_closing)
main_window.title("Убийца WarShips")
main_window.geometry('680x360+900+400')
main_window.resizable(False,False)
main_window.wm_attributes("-topmost", 1)

miss = tk.PhotoImage(file="data/miss.png")
water = tk.PhotoImage(file="data/water.png")
cell = tk.PhotoImage(file="data/cell.png")
fire = tk.PhotoImage(file="data/fire.png")
kill = tk.PhotoImage(file="data/kill.png")
player_ship = tk.PhotoImage(file="data/player_ship.png")
screen_game = tk.PhotoImage(file="data/screen_game.png")

my_cell = create_board(my_cell, cell)
enemy_cell = create_board(enemy_cell, water)

logo_game = tk.Label(main_window, image=screen_game)

btn_connect = tk.Button(main_window, text='Connect', command= connect_btn)
btn_random = tk.Button(main_window, text='Random', command= random_btn)

btn_connect.place(x=280 , y=320 , width=120, height = 30)
logo_game.place(x=-2, y=-2)

main_window.mainloop()