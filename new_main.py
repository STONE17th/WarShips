import data_ship
import tkinter as tk
import net_func as nf
from tkinter import messagebox





class Game:
    def __init__(self, enemy_round,listen_sock):
        self.enemy_round = enemy_round
        self.listen_sock = listen_sock
        self.id = None


class Cell(tk.Button):
    def __init__(self, master, x: int, y: int, id, *args, **kwargs):
        super(Cell, self).__init__(master, *args, **kwargs)
        self.id = id
        self.x = x
        self.y = y

    # def coords(self):
    #     return (self.x, self.y)

    def open_cell(self):
        if game.enemy_round:
            return
        my_shoot = nf.send_fire(sb_client_sock, game.id, (self.x, self.y))
        match my_shoot[0]:
            case 0:
                # my_shoot_list[self.id] = False
                self['image'] = miss
                self['relief'] = tk.SUNKEN
                game.enemy_round = True
                nf.receive_fire(sb_client_sock, btn_connect, game)

            case 1:
                # my_shoot_list[self.id] = True
                self['image'] = fire
                self['relief'] = tk.SUNKEN
            case 2:
                #my_shoot_list[self.id] = True
                self['image'] = kill
                self['relief'] = tk.SUNKEN
                check_kill(my_shoot[1], my_shoot[2], my_shoot[3], my_shoot[4], enemy_cell)
            case 3:
                # messagebox.INFO('Победа!', 'Капитан, поздравляем! Мы надрали им зад!')
                print("Победа")
            case _:
                pass
        # my_shoot_list.append(my_shoot)
        # self['text'] = ''
        # if self.id in ships_position: self['image'] = ship_new
        # else: self['image'] = miss
        # self['relief'] = tk.SUNKEN
        # print((self.x, self.y, self.id))
        # print(my_cell[45].id, my_cell[45].x, my_cell[45].y)

    # def round_shooting(self, board):
    #     buffer = [-1, 0, 1]
    #     for i in buffer:
    #         for j in buffer:
    #             temp_x, temp_y = self.y, self.x
    #             temp_x += i
    #             temp_y += j
    #             board[xy_to_id(temp_x, temp_y, cell_xy)]['relief'] = tk.SUNKEN
    #             board[xy_to_id(temp_x, temp_y, cell_xy)]['image'] = miss
    #             board[xy_to_id(temp_x, temp_y, cell_xy)]['state'] = tk.DISABLED

    def __repr__(self):
        return 'Cell'


class Ship(tk.Canvas):
    def __init__(self, master, cells, x, y, size, direct, *args, **kwargs):
        super(Ship, self).__init__(master, *args, **kwargs)
        self.size = size
        self.direct = direct
        self.x = x
        self.y = y
        self.cells = []

    def init_ship_cells(self):
        self.cells.clear()
        cur_x, cur_y = self.x, self.y
        for _ in range(self.size):
            self.cells.append((cur_x, cur_y))
            if self.direct == 0: cur_x += 1
            else: cur_y += 1

    def change_dir(self):
        if self.direct == 1:
            self.direct = 0
        else: self.direct = 1

    def __repr__(self):
        return 'Ship'


def on_closing():
    if messagebox.askyesno("Уходите?", "Вы хотите нас покинуть?"):
        if sb_client_sock != None:
            nf.disconnect_sock(sb_client_sock)
        main_window.destroy()

# =================================== КОМАНДЫ КНОПОК ==================================================================

def connect_btn():
    global sb_client_sock, player_ships
    sb_client_sock = nf.connect_to_host('localhost', 9091)
    if nf.check_connection(sb_client_sock):
        set_field(my_cell, 0)
        player_ships = shipyard()
        btn_random.place(x=370, y=280, width=300, height=30)
        logo_game.destroy()
        btn_connect['command'] = ready_btn
        btn_connect['text'] = 'Ready?'
    # set_field(my_cell, 0)

def send_btn():
    if data_ship.out_of_shipyard(player_ships):
        btn_random.destroy()
        set_field(enemy_cell, 1)
        send_ship_position(player_ships)
        coords_ships = []
        for ship in player_ships:
            coords_ships.append((ship.size, ship.direct, ship.x, ship.y))
        print(coords_ships)
        if nf.send_field(sb_client_sock, coords_ships):
            # disable_player_ships()
            # disable_player_field(my_cell)
            btn_connect['command'] = find_btn
            btn_connect['text'] = 'Найти соперника'

def ready_btn():
    if nf.start_game(sb_client_sock):
        btn_connect['command'] = send_btn
        btn_connect['text'] = 'Send Field'

def find_btn():
    print(game.id)
    if game.id == None:
        nf.find_player(sb_client_sock, btn_find, game)
    else:
        nf.receive_fire(sb_client_sock, btn_find, game)
    btn_connect['state'] = tk.DISABLED
    btn_connect['text'] = 'Поиск соперника'
    # btn_find['command'] = lambda: nf.receive_fire(sb_client_sock, btn_find, game)


def random_btn():
    global ships_position
    ships_position = data_ship.random_ship_position(player_ships, cell_xy)
    print(ships_position)


# =========================================== ФУНКЦИИ СЕРВЕРА ==================================================



# my_cell = []
# enemy_cell = []
# # enemy_map = []
# # my_shoot_list = []
# player_ships = []
# # ships_position = []
#
# cell_xy = {}
# game = Game(False,False)
#
# sb_client_sock = None



# def print_id(cell: Cell):
#     print(cell.id, cell.x, cell.y)


def create_board (board: list, image: any):
    ind = 0
    for i in range(12):
        for j in range(12):
            if i == 0 or j == 0 or i == 11 or j == 11: board.append(Cell(main_window, id=0, x=0, y=0))
            else:
                board.append(Cell(main_window, id=ind, x=i, y=j, image=image))
            ind += 1
    return board


def set_field(field, n):
    for i in range(144):
        if not field[i].id == 0:
            cell_xy[i] = (field[i].x, field[i].y)
            x = 10 + (field[i].x- 1)*30 + n*360
            y = 10 + (field[i].y -1)*30
            field[i].place(x=x, y=y, width=30, height=30)
            field[i]['command'] = field[i].open_cell


def shipyard():
    player_ships = []
    s = 4
    n = 0
    space_y = 0
    while s:
        space_x = 0
        for i in range(s):
            k = 5 - s
            player_ships.append(Ship(main_window,cells=[], x=11 , y=11, width=30, height=30 * s, size=k, direct=0, bg='GRAY'))
            player_ships[n].place(x=370 + 30 * (i*player_ships[n].size)+space_x, y=10 + 30*(4-s) + space_y, width=player_ships[n].size * 30, height=30)
            space_x += 30
            n += 1
        space_y += 30
        s = s - 1
    for ship in player_ships:
        ship.bind('<B1-Motion>', ship_drag)
        ship.bind('<Button-3>', ship_rotate)
        ship.bind('<Button-2>', ship_view)
    return player_ships

def ship_drag(event):
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

def ship_view(event):
    print(event.widget.x, event.widget.y, event.widget.size, event.widget.direct)

# def ship_rotate_random(ship):
#     ship.change_dir()
#     wid_w = ship.place_info().get('width')
#     wid_h = ship.place_info().get('height')
#     ship.place(width= wid_h)
#     ship.place(height= wid_w)

def send_ship_position(player_ships):
    for ship in player_ships:
        ship_x = ship.place_info().get('x')
        ship_y = ship.place_info().get('y')
        ship_x = ((int(ship_x) + 10) // 30) * 30 + 10
        ship_y = ((int(ship_y) + 10) // 30) * 30 + 10
        ship.x = int((ship_x - 10) / 30 + 1)
        ship.y = int((ship_y - 10) / 30 + 1)

# def out_of_shipyard(ship_position):
#     for ship in ship_position:
#         if ship.direct:
#             if ship.x > 11 or ship.y + ship.size > 11:
#                 print(ship.x, ship.y, ship.size)
#                 messagebox.showinfo('Капитан!', 'Капитан, мы не можем отправить расположение кораблей! Не все корабли в зоне действий!')
#                 return False
#         else:
#             if ship.x + ship.size > 11 or ship.y > 11:
#                 print(ship.x, ship.y, ship.size)
#                 messagebox.showinfo('Капитан!', 'Капитан, мы не можем отправить расположение кораблей! Не все корабли в зоне действий!')
#                 return False
#     return True

def xy_to_id(x, y, dictionary):
    k = [k for k, v in dictionary.items() if v == (y, x)]
    if k == []: return 0
    else: return int(k[0])

def round_shooting(x, y, enemy_board):
    buffer = [-1, 0, 1]
    for i in buffer:
        for j in buffer:
            temp_x, temp_y = y, x
            temp_x += i
            temp_y += j
            # print(temp_x, temp_y, i , j)
            # print(xy_to_id(temp_x, temp_y, cell_xy))
            enemy_board[xy_to_id(temp_x, temp_y, cell_xy)]['relief'] = tk.SUNKEN
            enemy_board[xy_to_id(temp_x, temp_y, cell_xy)]['image'] = miss
            # enemy_board[xy_to_id(temp_x, temp_y, cell_xy)]['state'] = tk.DISABLED
    enemy_board[xy_to_id(y, x, cell_xy)]['image'] = kill

def around_ship_size(size, direct, x, y, enemy_board):
    fire_x, fire_y = x, y
    for _ in range(size):
        round_shooting(fire_x, fire_y, enemy_board)
        if direct: fire_y += 1
        else: fire_x += 1
    fire_x, fire_y = x, y
    for _ in range(size):
        enemy_board[xy_to_id(fire_y, fire_x, cell_xy)]['image'] = kill
        if direct: fire_y += 1
        else: fire_x += 1

def check_kill(size, direct, x, y, enemy_board):
    if size == 1:
        round_shooting(x, y, enemy_board)
        # enemy_board[xy_to_id(fire_x,fire_y, cell_xy)]['image'] = kill
    else:
        around_ship_size(size, direct, x, y, enemy_board)
        # if direct:
        #     fire_x, fire_y = x, y
        #     for _ in range(size):
        #         round_shooting(fire_x,fire_y, enemy_board)
        #         fire_y += 1
        #     fire_x, fire_y = x, y
        #     for _ in range(size):
        #         enemy_board[xy_to_id(fire_y, fire_x, cell_xy)]['image'] = kill
        #         fire_y += 1
        # else:
        #     fire_x, fire_y = x, y
        #     for _ in range(size):
        #         round_shooting(fire_x,fire_y, enemy_board)
        #         fire_x += 1
        #     fire_x, fire_y = x, y
        #     for _ in range(size):
        #         enemy_board[xy_to_id(fire_y, fire_x, cell_xy)]['image'] = kill
        #         fire_x += 1


# my_cell = create_board(my_cell, cell)
# enemy_cell = create_board(enemy_cell, water)

my_cell = []
enemy_cell = []
# enemy_map = []
# my_shoot_list = []
player_ships = []
# ships_position = []

cell_xy = {}
game = Game(False,False)

sb_client_sock = None

main_window = tk.Tk()
main_window.protocol('WM_DELETE_WINDOW', on_closing)
main_window.title("Убийца WarShips")
main_window.geometry('680x360+900+400')
main_window.resizable(False,False)
main_window.wm_attributes("-topmost", 1)

# miss = tk.PhotoImage(file="data/miss_small.png")
# water = tk.PhotoImage(file="data/water.png")
# cell = tk.PhotoImage(file="data/free_cell_water.png")
# ship_new = tk.PhotoImage(file="data/ship.png")
# fire = tk.PhotoImage(file="data/fire.png")
# kill = tk.PhotoImage(file="data/kill.png")
# screen_game = tk.PhotoImage(file="data/screen_game.png")


# my_cell = create_board(my_cell, cell)
# enemy_cell = create_board(enemy_cell, water)

# logo_game = tk.Label(main_window, image=screen_game)

#
#
# btn_connect = tk.Button(main_window, text='Connect', command= connect_btn)
# btn_send = tk.Button(main_window, text='Send', command= send_btn)
# btn_ready = tk.Button(main_window, text='Ready', command= ready_btn)
# btn_find = tk.Button(main_window, text='Find', command= find_btn)
# btn_random = tk.Button(main_window, text='Random', command= random_btn)
#
# # btn_send.place(x=40 , y=320 , width=90, height = 30)
# # btn_find.place(x= 190, y=320, width=90, height = 30)
# btn_connect.place(x=280 , y=320 , width=120, height = 30)
# logo_game.place(x=-2, y=-2)
# # btn_ready.place(x= 390, y=320, width=90, height = 30)
#
#
# main_window.mainloop()

miss = tk.PhotoImage(file="data/miss_small.png")
water = tk.PhotoImage(file="data/water.png")
cell = tk.PhotoImage(file="data/free_cell_water.png")
ship_new = tk.PhotoImage(file="data/ship.png")
fire = tk.PhotoImage(file="data/fire.png")
kill = tk.PhotoImage(file="data/kill.png")
screen_game = tk.PhotoImage(file="data/screen_game.png")

my_cell = create_board(my_cell, cell)
enemy_cell = create_board(enemy_cell, water)

logo_game = tk.Label(main_window, image=screen_game)

btn_connect = tk.Button(main_window, text='Connect', command= connect_btn)
btn_send = tk.Button(main_window, text='Send', command= send_btn)
btn_ready = tk.Button(main_window, text='Ready', command= ready_btn)
btn_find = tk.Button(main_window, text='Find', command= find_btn)
btn_random = tk.Button(main_window, text='Random', command= random_btn)

# btn_send.place(x=40 , y=320 , width=90, height = 30)
# btn_find.place(x= 190, y=320, width=90, height = 30)
btn_connect.place(x=280 , y=320 , width=120, height = 30)
logo_game.place(x=-2, y=-2)
# btn_ready.place(x= 390, y=320, width=90, height = 30)


main_window.mainloop()