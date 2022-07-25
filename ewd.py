ship_list = [[4], [17, 27], [19, 29], [21, 22, 23, 24], [51], [53, 63, 73], [55, 65, 75], [58, 59], [78], [81]]
while True:
    print(ship_list)
    shoot = int(input("Куда стреляем? "))
    hit = False
    for ship in ship_list:
        for cell in ship:
            if shoot == cell:
                ship.remove(cell)
                if len(ship) == 0:
                    print('Убил!')
                    ship_list.remove(ship)
                else: print('Ранил')
                hit = True
    if not hit: print('Мимо...')

    print(ship_list)
