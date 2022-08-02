import socket
import threading


def send_field(sock: socket, ships_data: list) -> bool:
    data_to_send = bytearray()
    data_to_send.append(2)

    for elem in ships_data:
        data_to_send += bytes(elem)
    sock.send(data_to_send)
    data = sock.recv(1024)
    print(data)
    if data == bytes((2, 0)):
        return True
    else:
        return False


def send_fire(sock: socket,id: int, coords: tuple) -> tuple:  # возвращает 0 - мимо, 1 - попал, 2 - потопил, 3 - победил

    sock.send(bytes((3, id, coords[0], coords[1])))

    data = sock.recv(1024)
    print(data)

    if data[0] == 3:
        if data[1] == 0:
            return tuple(data[2:])
        else:
            return False


def start_game(sock) -> bool:
    sock.send(bytes((4,)))

    data = sock.recv(1024)
    print(data)

    if data == bytearray((4, 0)):
        return True
    else:
        return False


def find_player(sock, view_obj, gameobj) -> str:
    sock.send(bytes((6,)))

    data = sock.recv(1024)
    print(data)

    if data[0] == 6:
        if (data[1]) == 0:
            wait_game(sock, view_obj, gameobj)

            return True
        return False
    else:
        return False


def connect_to_host(addr: str, port: int) -> socket:
    sb_client_sock = socket.socket()
    sb_client_sock.connect((addr, port))

    return sb_client_sock


def check_connection(sock: socket) -> bool:
    sock.send(bytes((1,)))

    data = sock.recv(1024)
    print(data)
    if data == bytearray((1, 0)):
        return True
    else:
        return False


def disconnect_sock(sock: socket) -> bool:
    if sock != None:
        sock.send(bytes((5,)))

    data = sock.recv(1024)
    print(data)
    if data == bytearray((5, 0)):
        sock.close()
        return True
    else:
        return False


def receive_fire(sock, view_obj, gameobj):
    def listen_data(sock, view_obj, gameobj):
        # print('im a thread')
        # print(gameobj.enemy_round)
        # print(gameobj.listen_sock)
        gameobj.listen_sock = True
        view_obj['text'] = 'Ход врага'
        data = sock.recv(1024)
        # print(data)

        while data[1] == 1 or data[1] == 2:
            data = sock.recv(1024)
            print(data)
            gameobj.enemy_round = True
            view_obj['text'] = 'Ход врага'

        gameobj.listen_sock = False
        gameobj.enemy_round = False
        if data[1] == 3:
            view_obj['text'] = 'Ты проиграл'
        else:
            view_obj['text'] = 'Твой ход'
            gameobj.enemy_round = False
    if not gameobj.listen_sock:
        thread = threading.Thread(target=listen_data, name='listen_data', args=(sock, view_obj, gameobj))
        thread.start()
        print('Thread started')
    else:
        pass


def wait_game(sock, view_obj, gameobj):
    def listen_data(sock, view_obj, gameobj):
        gameobj.listen_sock = True
        view_obj['text'] = 'Поиск игры'
        data = sock.recv(1024)
        # print(data)
        if data[0] == 7:
            gameobj.id = data[1]
            view_obj['text'] = 'Игра началась'
            gameobj.enemy_round = bool(data[2])
            if gameobj.enemy_round:
                # receive_fire(sock, view_obj, gameobj)
                view_obj['text'] = 'Ход врага!'
            else: view_obj['text'] = 'Твой ход!'
    if not gameobj.listen_sock:
        thread = threading.Thread(target=listen_data, name='listen_data', args=(sock, view_obj, gameobj))
        thread.start()
    else:
        pass