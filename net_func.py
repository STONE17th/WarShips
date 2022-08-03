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
            return (4,)


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


def disconnect_sock(sock: socket, id) -> bool:
    if sock != None:
        data_to_send = (bytes((5,id)))
        print(data_to_send)
        sock.send(data_to_send)

    data = sock.recv(1024)
    print(data)
    if data == bytearray((5, 0)):
        sock.close()
        return True
    else:
        return False


def receive_fire(sock, view_obj, gameobj):

    def listen_data(sock, view_obj, gameobj):
        gameobj.listen_sock = True
        view_obj['text'] = 'Ход врага'
        
        while gameobj.enemy_round:
            data = sock.recv(1024)
            print(data)
            gameobj.listen_sock = False
            if data[0] == 8:
                gameobj.enemy_shoot_list.append((data[2],data[3]))
                if data[1] == 0:
                    gameobj.enemy_round = False                    
                    view_obj['text'] = 'Твой ход'
                elif data[1] == 3:
                    view_obj['text'] = 'Ты проиграл'
                    gameobj.enemy_round = False

            elif data[0] == 9:

                gameobj.enemy_round = False
                view_obj['text'] = 'Противник сдался'
        print('receive_fire finished')

    if not gameobj.listen_sock:
        thread = threading.Thread(target=listen_data, name='listen_data', args=(sock, view_obj, gameobj))
        thread.start()
        print('Thread receive fire started')
    else:
        pass


def wait_game(sock, view_obj, gameobj):
    def listen_data(sock, view_obj, gameobj):
        gameobj.listen_sock = True
        view_obj['text'] = 'Поиск игры'
        data = sock.recv(1024)
        gameobj.listen_sock = False
        print(data)
        if data[0] == 7:
            gameobj.id = data[1]
            view_obj['text'] = 'Игра началась'
            gameobj.enemy_round = bool(data[2])
            if gameobj.enemy_round:
                # receive_fire(sock, view_obj, gameobj)
                view_obj['text'] = 'Ход врага!'
                receive_fire(sock, view_obj, gameobj)
            else: view_obj['text'] = 'Твой ход!'
            print('wait_game finished')
            
            
    if not gameobj.listen_sock:
        thread = threading.Thread(target=listen_data, name='listen_data', args=(sock, view_obj, gameobj))
        thread.start()
        print('Thread wait game started')
    else:
        pass