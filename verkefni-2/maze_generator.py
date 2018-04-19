# maze generator for maze game
# örn óli strange
from random import choice, randint, randrange

destroy_some_walls = True

def make_2d_array(rows, columns=False):
    # 2d array function
    if not columns:
        columns = rows
    return [[[True, False] for row in range(rows)] for column in range(columns)]


def generate_maze(size):
    # maze vars
    maze_count = size
    if maze_count % 2 == 0:
        maze_count += 1
    maze_array = make_2d_array(maze_count)

    # Make walls for maze
    for i in range(1, maze_count - 1):
        for j in range(1, maze_count - 1):
            if i % 2 != 0 and j % 2 != 0:
                maze_array[i][j] = [False, False]

    def all_visited():
        for i in range(1, maze_count - 1):
            for j in range(1, maze_count - 1):
                if i % 2 != 0 and j % 2 != 0 and not maze_array[i][j][1]:
                    return False
        return True

    def random_current():
        for i in range(1, maze_count - 1):
            for j in range(1, maze_count - 1):
                if i % 2 != 0 and j % 2 != 0 and not maze_array[i][j][1]:
                    return i, j

    stack = []

    # main loop
    current = random_current()
    while not all_visited():
        available_sets = []
        maze_array[current[0]][current[1]][1] = True
        if current[0] + 2 < maze_count - 1:
            if not maze_array[current[0] + 2][current[1]][1]:
                available_sets.append((current[0] + 2, current[1]))
        if current[0] - 2 > 0:
            if not maze_array[current[0] - 2][current[1]][1]:
                available_sets.append((current[0] - 2, current[1]))
        if current[1] + 2 < maze_count - 1:
            if not maze_array[current[0]][current[1] + 2][1]:
                available_sets.append((current[0], current[1] + 2))
        if current[1] - 2 > 0:
            if not maze_array[current[0]][current[1] - 2][1]:
                available_sets.append((current[0], current[1] - 2))
        if len(available_sets) > 0:
            new_current = choice(available_sets)
            middle = (int((current[0] + new_current[0]) / 2), int((current[1] + new_current[1]) / 2))
            maze_array[middle[0]][middle[1]][0] = False
            stack.append(current)
            current = new_current
        else:
            if len(stack) > 0:
                current = stack.pop()

    # enter
    maze_array[0][1][0] = False

    if destroy_some_walls:
        for i in range(1, maze_count-3):
            if randint(0, 3) > 0:
                maze_array[i][randrange(1, maze_count-2, 2)][0] = False
                maze_array[i][randrange(1, maze_count-2, 2)][0] = False
                maze_array[i][randrange(1, maze_count - 2, 2)][0] = False

    # return maze
    final_maze_list = []
    maze_list = [sublist for sublist in maze_array]
    for i in maze_list:
        final_maze_list.append(list(map(lambda x: x[0], i)))
    return final_maze_list