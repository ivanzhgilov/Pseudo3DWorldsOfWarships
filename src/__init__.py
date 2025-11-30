import src.consts

MAP_SIZE = src.consts.MAP_SIZE

array_reserve = []
array_can_use = []

for i in range(MAP_SIZE):
    for j in range(MAP_SIZE):
        if (
            i == 0
            or i == MAP_SIZE - 1
            or j == 0
            or j == MAP_SIZE - 1
            or (16 <= i <= 18 and 16 <= j <= 18)
        ):
            array_reserve.append((i, j))
        else:
            array_can_use.append((i, j))

src.consts.RESERVED_CELLS = array_reserve
src.consts.START_CAN_USE_CELLS = array_can_use
