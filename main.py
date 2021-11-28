def create_pole(NxN):
    # Создаем начальное поле
    matrix = [[chr(96 + j) if i == 0 else (str(i) if j == 0 else "_") for j in range(NxN + 1)] for i in range(NxN + 1)]
    matrix[0][0] = ""

    # создаем начальный список свободных ходов
    free_turns = [j + i for j in
                  "".join(map(str, (range(1, NxN + 1)))) for i in "".join(map(str, (range(1, NxN + 1))))]
    return matrix, free_turns


def make_items_for_check(pole):
    column = diagm = diagr = ""
    diags_main = []
    diags_reverse = []
    raws = []
    columns = []
    # формируем списки строк, столбцов
    for i in range(1, len(pole)):
        raw = "".join(pole[i][1:])
        for j in range(1, len(pole)):
            column += pole[j][i]
        columns.append(column)
        raws.append(raw)
        column = ""
    # формируем списки основных и побочных диаганалей
    for step in range(len(pole) - 3):
        for i in range(len(pole) - 3):
            for j in range(1, 4):
                diagr += pole[len(pole) - j - i][j + step]
                diagm += pole[j + i][j + step]
            diags_main.append(diagm)
            diags_reverse.append(diagr)
            diagm = diagr = ""

    return raws, columns, diags_main, diags_reverse


# Отображение игрового поля
def show_game(pole):
    print()
    for raw in pole:
        raw = list(map(lambda x: x.ljust(2), raw))
        print(*raw)


# логика хода ИИ
def ii_turn(pole, free_turns, pl_item, ii_item):
    from random import randrange
    flag_random = True
    flag_ii = True
    raws, columns, diags_main, diags_reverse = make_items_for_check(pole)

    # функция преоразования хода в индексы поля и отображение хода на поле
    def operation(turn):
        x = int(turn[0])
        y = int(turn[1])
        pole[x][y] = ii_item
        nonlocal flag_ii
        nonlocal flag_random
        flag_ii = False
        flag_random = False

        # ходы атаки

    for i in range(len(raws)):
        # ход строки
        if all([raws[i].count(ii_item) == 2, raws[i].count("_") == len(pole) - 3, flag_ii]):
            turn = str(i + 1) + str(raws[i].index("_") + 1)
            operation(turn)
        # ход столбцы
        elif all([columns[i].count(ii_item) == 2, columns[i].count("_") == len(pole) - 3, flag_ii]):
            turn = str(columns[i].index("_") + 1) + str(i + 1)
            operation(turn)

    for i in range(len(diags_main)):
        # ход главная диаганаль
        if all([diags_main[i].count(ii_item) == 2, diags_main[i].count("_") == len(pole) - 3, len(pole) == 4, flag_ii]):
            turn = str(diags_main[i].index("_") + 1) * 2
            operation(turn)
        # ход побочная диаганаль
        elif all([diags_reverse[i].count(ii_item) == 2, diags_reverse[i].count("_") == len(pole) - 3, len(pole) == 4,
                  flag_ii]):
            turn = str(len(pole) - diags_reverse[i].index("_") - 1) + str(diags_reverse[i].index("_") + 1)
            operation(turn)

    # ходы защиты
    for i in range(len(raws)):
        # ход строки
        if all([raws[i].count(pl_item) == 2, raws[i].count("_") == len(pole) - 3, flag_ii]):
            turn = str(i + 1) + str(raws[i].index("_") + 1)
            operation(turn)
        # ход столбцы
        elif all([columns[i].count(pl_item) == 2, columns[i].count("_") == len(pole) - 3, flag_ii]):
            turn = str(columns[i].index("_") + 1) + str(i + 1)
            operation(turn)
    for i in range(len(diags_main)):
        # ход главная диаганаль
        if all([diags_main[i].count(pl_item) == 2, diags_main[i].count("_") == len(pole) - 3, len(pole) == 4, flag_ii]):
            turn = str(diags_main[i].index("_") + 1) * 2
            operation(turn)
            # ход побочная диаганаль
        elif all([diags_reverse[i].count(pl_item) == 2, diags_reverse[i].count("_") == len(pole) - 3, len(pole) == 4,
                  flag_ii]):
            turn = str(len(pole) - diags_reverse[i].index("_") - 1) + str(diags_reverse[i].index("_") + 1)
            operation(turn)

    # занимаем центр 1м ходом
    if pole[len(pole) // 2 + len(pole) % 2][len(pole) // 2 + len(pole) % 2] == "_":
        pole[len(pole) // 2 + len(pole) % 2][len(pole) // 2 + len(pole) % 2] = ii_item
        turn = str(len(pole) // 2 + len(pole) % 2) * 2
        flag_random = False
    # рандом ходы
    if flag_random and len(free_turns) >= 2:
        turn = free_turns[randrange(1, len(free_turns))]
        operation(turn)
    # оставшийся последний ход
    if len(free_turns) < 2:
        turn = free_turns[0]
        operation(turn)

    return turn, pole


# Ход игрока
def player_turn(pole, pl_item):
    # словарь для преобразования введеного игроком хода в индексы игрового поля
    d_columns = {chr(96 + i): i for i in range(1, len(pole))}
    d = d_columns.copy()
    d_raws = {str(i): i for i in range(1, len(pole))}
    d.update(d_raws)

    flag = False
    while not flag:
        turn = input("\nваш ход: ").lower()
        # проверка на длину вводимых данных
        if len(turn) != 2:
            print("\nход введен не корректно!")
            continue
        # если ход начинается с цифры то меняем символы местами, приводим к формату A1
        if turn[0].isdigit():
            turn = turn[::-1]
        column = turn[0]
        raw = turn[1]
        turn = "".join(map(lambda x: x if x not in d else str(d[x]), turn[::-1]))
        # проверка попадает ли введеный ход на поле
        if column in d_columns.keys() and raw in d_raws.keys():
            # проверка свободно ли место на поле
            if pole[d[raw]][d[column]] != "_":
                print("\nсюда уже ходили")
            else:
                pole[d[raw]][d[column]] = pl_item
                flag = True
        else:
            print("\nход введен не корректно")

    return turn, pole


# Проверка результата игры
def end_game(pole, turns, pl_item, ii_item, wins, loses):
    flag_end = False
    grats = "\nПоздравляем, Вы победили!!!\n"
    shame = "\nВы проиграли :(\n"
    wtf = "\nНичья...\n"
    gg = pl_item * 3
    bg = ii_item * 3
    # формируем строки, столбцы, диаганали
    raws, columns, diags_main, diags_reverse = make_items_for_check(pole)
    all_items = raws + columns + diags_main + diags_reverse
    for target in all_items:
        # проверка выигрыша
        if gg in target:
            print(grats)
            flag_end = True
            wins += 1
            break
        # проверка проигрыш
        if bg in target:
            print(shame)
            flag_end = True
            loses += 1
            break
        # проверка ничья
    if len(turns) == 0 and not flag_end:
        print(wtf)
        flag_end = True
    return flag_end, wins, loses


def decorator(fn):
    from time import time
    t0 = time()

    def wrapper(*args, **kwargs):
        global t
        res = fn(*args, **kwargs)
        t = time() - t0
        return res

    return wrapper


@decorator
def game(NxN, pl_item, w=0, ls=0, gs=0):
    wins = w
    loses = ls
    games = gs
    moves = 0
    game_continie = False
    finish = ""
    flag_end = False
    items = ["x", "0"]
    if any([pl_item not in items, NxN not in range(3, 6)]):
        flag_end = True
        print("игра запущена с неверными параметрами")
    else:
        d = {str(i + 1): chr(97 + i) for i in range(NxN)}
        items.remove(pl_item)
        ii_item = "".join(items)
        pole, free_turns = create_pole(NxN)
        print(f"\n\t  Счет игры\nВы: {wins} \tПротивник: {loses}\t партий: {games}")
        print(f"\nвы играете {pl_item.upper()}")
        if games % 2 == 0:
            show_game(pole)

    while not flag_end:
        # игрок ходит каждую нечетную игру 1-м, а четную игру со 2го хода
        if games % 2 == 0 or games % 2 != 0 and moves > 0:
            turn, pole = player_turn(pole, pl_item)
            show_game(pole)
            free_turns.remove(turn)
            flag_end, wins, loses = end_game(pole, free_turns, pl_item, ii_item, wins, loses)
            moves += 1
        # ход противника
        if not flag_end:
            turn, pole = ii_turn(pole, free_turns, pl_item, ii_item)
            print(f"\nход противника: {d[turn[0]]}{turn[1]}")
            show_game(pole)
            free_turns.remove(turn)
            flag_end, wins, loses = end_game(pole, free_turns, pl_item, ii_item, wins, loses)
            moves += 1

    games += 1

    while not finish:
        if moves == 0:
            break
        finish = input('чтобы продолжить игру введите "Y" иначе введите "N":').lower()
        if finish not in ("y", "у", "n"):
            print("ошибка ввода")
            finish = ""
        if finish in ("y", "у"):
            game_continie = True
        elif finish == "n":
            game_continie = False

    if game_continie:
        return game(NxN, pl_item, w=wins, ls=loses, gs=games)
    elif moves != 0:
        print(f"\n\nигры закончались с результатом\nВы: {wins} \tПротивник: {loses}\tпартий: {games} \n")


t = 0  # глобальная переменная, куда будет перезаписано общее время работы программы

# опции игры
# pl_item - выбор чем будет играть игрок
# NxN - размер поля от 3 до 5
game(pl_item="x", NxN=3, w=0, ls=0, gs=0)
if t > 1:
    print(f"игры длились {t // 60:.0f} минут(ы) {t % 60:.0f} секунд(ы)")
