import socket
import threading
import time
from .game_controller import *

class SB_server():

    def __init__(self,laddr,lport):
        self.laddr = laddr
        self.lport = lport
        self.t_accept_con = None
        self.server_sock = None
        self.sock_con = {}
        self.t_data_recv = []
        self.players_status = {} # 0 - подключен 1 - поиск игры 2 - в игре
        self.players_ships = {}
        self.players_fields = {}
        self.games = {}


   
    def init_sock(self):
        self.server_sock = socket.socket()
        self.server_sock.bind((self.laddr,self.lport))
        self.server_sock.listen(0)   


    def accept_con(self):
        while True:
            con_sock,addr = self.server_sock.accept()
            print(f'Connected {addr}')
            self.sock_con[con_sock.getpeername()] = con_sock
            self.thread_data_recv(con_sock,addr) 

    
    def thread_accept_con(self):
        if self.t_accept_con == None:
            thread = threading.Thread(target=self.accept_con,name='accept_con')
            self.t_accept_con = thread
            thread.start()
            print(thread.ident,f'started. Listening on {self.laddr}:{self.lport}')
        else:
            print(thread.ident,'already started')


    def thread_data_recv(self, socket, addr):
        print(f'Starting data transfer {addr}')
        thread = threading.Thread(target=self.data_transfer,name='data_recv',args=(socket,))
        self.t_data_recv.append(thread)
        thread.start()

    
    def data_transfer(self, sock):
        while sock.fileno() != -1:
            data = sock.recv(1024)
            print(data)

            if not data:
                sock.close()

            else:
                try:
                    self.decode_data(sock, data)
                except:
                    pass
    

    def get_field(self, sock, sock_name, data):

        if (sock_name not in self.players_status.keys()) or self.players_status[sock_name] != 0:
            sock.send(bytes((2,1)))
            return
        else:
            ships = get_ships(data)
            self.players_ships[sock_name] = ships
            self.players_fields[sock_name] = Field(ships)
            sock.send(bytes((2,0)))


    def check_fire(self, enemy_player, game_id, coords):

        if coords in self.players_fields[enemy_player].field.keys():
            ship_id = self.players_fields[enemy_player].field[coords]
            enemy_ship = self.players_ships[enemy_player][ship_id]
            ship_cells = enemy_ship.cells
            ship_cells.discard(coords)
            if len(ship_cells) == 0:
                self.games[game_id].score[enemy_player] += 1
                if self.games[game_id].score[enemy_player] == 10:
                    self.sock_con[enemy_player].send(bytes((8,3,coords[0],coords[1])))
                    return (3,) + enemy_ship.dump()
                else:
                    self.sock_con[enemy_player].send(bytes((8,2,coords[0],coords[1])))
                    return (2,) + enemy_ship.dump()
            else:
                self.sock_con[enemy_player].send(bytes((8,1,coords[0],coords[1])))
                return (1,)
        else:
            self.sock_con[enemy_player].send(bytes((8,0,coords[0],coords[1])))
            self.games[game_id].turn = enemy_player
            return (0,)


    def get_fire(self, sock, sock_name, data):
        
        game_id = data[1]
        enemy_player = self.games[game_id].enemy[sock_name]
        coords = tuple(data[2:])
        if self.games[game_id].turn == sock_name:

            sock.send(bytes((3,0) + self.check_fire(enemy_player, game_id, coords)))             

        else:
            sock.send(bytes((3,1)))


    def decode_data(self, sock, data):
        sock_name = sock.getpeername()
        match data[0]:
            case 1:
                sock.send(bytes((1,0)))
            case 2:
                self.get_field(sock, sock_name, data) 
            case 3:
                self.get_fire(sock, sock_name, data)
            case 4:
                self.players_status[sock_name] = 0
                sock.send(bytes((4,0)))
            case 5:
                
                game_id = data[1]
                print(game_id)
                if sock_name in self.players_ships.keys():
                    del self.players_ships[sock_name]
                
                if sock_name in self.players_fields.keys():
                    del self.players_fields[sock_name]

                if sock_name in self.players_status.keys():
                    del self.players_status[sock_name]
                
                if sock_name in self.sock_con.keys():
                    del self.sock_con[sock_name]

                if game_id > 0:
                    
                    try:
                        enemy_player_sock = self.sock_con[self.games[game_id].enemy[sock_name]]
                    # to do
                        enemy_player_sock.send(bytes((9,)))
                    except:
                        pass

                sock.send(bytes((5,0)))
                sock.shutdown()
                sock.close()
            case 6:
                if sock_name not in self.players_status.keys():
                    sock.send(bytes((6,1)))
                elif sock_name not in self.players_fields.keys():  
                    sock.send(bytes((6,1)))
                else:  
                    self.players_status[sock_name] = 1
                    sock.send(bytes((6,0)))    
                

            case 7:
                pass               
              
            case __:
                sock.send(bytes((0,)))          


    def game_create(self):
        finded_lst = []
        while True:
            finded_lst.clear()
            for elem in self.players_status.items():
                if elem[1] == 1:
                    finded_lst.append(elem[0])
                    if len(finded_lst) == 2:
                        new_game = Game(finded_lst[0], finded_lst[1])
                        self.games[new_game.id] = new_game
                        self.players_status[finded_lst[0]] = 2
                        self.players_status[finded_lst[1]] = 2
                        self.sock_con[finded_lst[0]].send(bytes((7, new_game.id, 0)))
                        self.sock_con[finded_lst[1]].send(bytes((7, new_game.id, 1)))
                        print(new_game.players)
                        finded_lst.clear()
            time.sleep(1)


    def thread_create_game(self):        
        thread = threading.Thread(target=self.game_create,name='game_create')
        print('Thread game started')
        thread.start()

