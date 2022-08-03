#!/usr/bin/python3

import server.server as server

srv = server.SB_server('0.0.0.0',9091)
srv.init_sock()
srv.thread_accept_con()
srv.thread_create_game()
while True:
    input()
    print(srv.sock_con)
    print()
    print(srv.players_status)
    print()
    print(srv.players_fields)
    print()
    print(srv.players_ships)
    print()
    print(srv.games)
    print()
