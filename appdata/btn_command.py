def connect_btn():
    global sb_client_sock, player_ships
    sb_client_sock = nf.connect_to_host('localhost', 9091)
    if nf.check_connection(sb_client_sock):
        set_field(my_cell, 0)
        player_ships = shipyard()
        btn_random.place(x=370, y=280, width=300, height=30)
        btn_connect['command'] = ready_btn
        btn_connect['text'] = 'Ready?'

def send_btn():
    btn_random.destroy()
    set_field(enemy_cell, 1)
    send_ship_position(player_ships)
    coords_ships = []
    for ship in player_ships:
        coords_ships.append((ship.size, ship.direct, ship.x, ship.y))
    print(coords_ships)
    if nf.send_field(sb_client_sock, coords_ships):
        btn_send['state'] = tk.DISABLED
        btn_send['text'] = 'OK'
        # disable_player_ships()
        # disable_player_field(my_cell)
        btn_random.destroy()

def ready_btn():
    if nf.start_game(sb_client_sock):
        btn_connect['state'] = tk.DISABLED
        btn_connect['text'] = 'READY!'

def find_btn():
    print(game.id)
    if game.id == None:
        nf.find_player(sb_client_sock, btn_find, game)
    else:
        nf.receive_fire(sb_client_sock, btn_find, game)
    # btn_find['command'] = lambda: nf.receive_fire(sb_client_sock, btn_find, game)


def random_btn():
    global ships_position
    ships_position = ship.random_ship_position(player_ships, cell_xy)
    print(ships_position)