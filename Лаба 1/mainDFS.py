import time
import tracemalloc


class Node:
    node_counter = 0

    def __init__(self, state, parent, action, path_cost, depth):
        self.id = Node.node_counter
        Node.node_counter += 1
        self.state = state
        self.parent = parent  # Ссылка на родительский узел
        self.action = action  # Действие, приведшее к этому узлу
        self.path_cost = path_cost  # Стоимость пути
        self.depth = depth  # Глубина

    def __repr__(self):
        parent_id = self.parent.id if self.parent else None
        return (f"Node ID: {self.id}, Parent ID: {parent_id}, Action: {self.action}, "
                f"Path-Cost: {self.path_cost}, Depth: {self.depth}, State:\n{self.state_str()}")

    def state_str(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.state)


def move(state, blank_pos, direction):
    new_state = [list(row) for row in state]  # Создаем копию состояния
    x, y = blank_pos
    if direction == "up": x, y = x - 1, y
    elif direction == "down": x, y = x + 1, y
    elif direction == "left": x, y = x, y - 1
    elif direction == "right": x, y = x, y + 1
    new_state[blank_pos[0]][blank_pos[1]], new_state[x][y] = new_state[x][y], new_state[blank_pos[0]][blank_pos[1]]
    return tuple(tuple(row) for row in new_state), (x, y)


def get_actions(x, y):
    actions = []
    if x > 0: actions.append("up")
    if x < 2: actions.append("down")
    if y > 0: actions.append("left")
    if y < 2: actions.append("right")
    return actions


def find_blank(state):
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            if cell == 0:
                return i, j


def dfs(start, goal):
    tracemalloc.start()  # Начало отслеживания памяти
    start_time = time.time()
    iterations = 0
    start_node = Node(start, None, None, 0, 0)
    stack = [start_node]
    visited = set()

    while stack:
        current_node = stack.pop()
        iterations += 1
        current_state = current_node.state

        if current_state == goal:
            end_time = time.time()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"Итераций потребовалось: {iterations}, Время выполнения: {end_time - start_time:.4f} секунд.")
            print(f"Пиковое использование памяти: {peak / 1024**2:.4f} MB")
            print(f"Всего создано узлов: {Node.node_counter}")
            return current_node

        visited.add(current_state)
        blank_pos = find_blank(current_state)
        for action in get_actions(*blank_pos):
            new_state, new_blank_pos = move(current_state, blank_pos, action)
            if new_state not in visited:
                child_node = Node(new_state, current_node, action, current_node.path_cost + 1, current_node.depth + 1)
                stack.append(child_node)

    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Остановка отслеживания памяти
    print(f"Итераций потребовалось: {iterations}, Время выполнения: {end_time - start_time:.4f} секунд.")
    print(f"Использование памяти: {peak / 1024**2:.4f} MB")
    print(f"Всего создано узлов: {Node.node_counter}")
    return None


def interactive_print(steps):
    choice = input("Выберите опцию вывода:\n1) Вывести все сразу\n2) Выводить каждый шаг после нажатия Enter\nВаш выбор: ")
    print("\nРешение:")
    if choice == "1":
        for step in steps:
            print(step)
            print("-" * 40)
    elif choice == "2":
        for step in steps:
            input("Нажмите Enter для вывода следующего шага...")
            print(step)
            print("-" * 40)
    else:
        print("Некорректный выбор. Выводим все сразу.")
        for step in steps:
            print(step)
            print("-" * 40)

    print("Вывод завершен. Программа будет закрыта.")


def print_solution(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    path.reverse()
    interactive_print(path)


start_state = ((0, 4, 3), (6, 2, 1), (7, 5, 8))
goal_state = ((1, 2, 3), (4, 0, 5), (6, 7, 8))

solution_node = dfs(start_state, goal_state)
print_solution(solution_node)
