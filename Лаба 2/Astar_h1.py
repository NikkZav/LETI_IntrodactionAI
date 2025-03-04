from collections import deque


class Node:
    node_counter = 0

    def __init__(self, state, parent=None, operator=None, path_cost=0, depth=0,
                 blank_pos: tuple[int, int] | None = None):
        self.id = Node.node_counter
        Node.node_counter += 1
        self.state = state
        self.blank_pos = blank_pos if blank_pos else self._get_blank_pos()
        self.operators = self._get_operators()
        self.parent = parent  # Ссылка на родительский узел
        self.action = operator  # Действие, приведшее к этому узлу
        self.path_cost = path_cost  # Стоимость пути
        self.depth = depth  # Глубина

    def move(self, operator):
        new_state = [list(row) for row in self.state]  # Создаем копию сост-я
        x_old, y_old = self.blank_pos
        if operator == "up":
            x_new, y_new = x_old - 1, y_old
        elif operator == "down":
            x_new, y_new = x_old + 1, y_old
        elif operator == "left":
            x_new, y_new = x_old, y_old - 1
        elif operator == "right":
            x_new, y_new = x_old, y_old + 1

        new_state[x_old][y_old], new_state[x_new][y_new] = \
            new_state[x_new][y_new], new_state[x_old][y_old]

        return tuple(tuple(row) for row in new_state), (x_new, y_new)

    def _get_blank_pos(self):
        for i, row in enumerate(self.state):
            for j, cell in enumerate(row):
                if cell == ' ':
                    return i, j

    def _get_operators(self):
        x, y = self.blank_pos
        operators = []
        if y > 0:
            operators.append("left")
        if x > 0:
            operators.append("up")
        if y < 2:
            operators.append("right")
        if x < 2:
            operators.append("down")
        return operators

    def __repr__(self):
        parent_id = self.parent.id if self.parent else None
        return (f"Node ID: {self.id}, Parent ID: {parent_id}, "
                f"Action: {self.action}, Path-Cost: {self.path_cost}, "
                f"Depth: {self.depth}, State:\n{self.state_str(self.state)}")

    @staticmethod
    def state_str(state):
        return '\n'.join(' '.join(str(cell) for cell in row)
                         for row in state)


class Problem:
    def __init__(self, init_state, goal_state, mode='step') -> None:
        self.init_state = init_state
        self.goal_state = goal_state
        self.count_new_states = 0  # количество полученных новых состояний
        self.visited: dict[tuple[tuple[int | str]], int] = {}
        self.mode = mode

    def goal_test(self, state):
        return state == self.goal_state

    def expand(self, node, operators) -> list[Node]:
        self.visited[node.state] = node.depth
        children = []
        for operator in operators:
            new_state, new_blank_pos = node.move(operator)
            self.count_new_states += 1
            if (new_state not in self.visited or
                    self.visited[new_state] > node.depth + 1):
                child_node = Node(new_state, node, operator,
                                  node.path_cost + 1,
                                  node.depth + 1,
                                  new_blank_pos)
                children.append(child_node)
            else:
                self.message(f"Состояние \n{Node.state_str(new_state)}\n"
                             "уже посещено")
        self.message("Добавленные после раскрытия новые вершины:",
                     *children, sep='\n')
        return children

    def message(self, *args, **kwargs):
        if self.mode != 'silent':
            print("-"*40)
            print(*args, **kwargs)
            print("-"*40)
        if self.mode == 'step':
            input("\nНажмите Enter для продолжения...\n")


def general_search(problem: Problem, queuing_fn):
    nodes = deque([Node(problem.init_state)])  # создаем кайму

    while True:
        if not nodes:
            raise Exception('нет решения !!!')

        node = nodes.popleft()
        problem.message(f"Текущая вершина, выбранная для раскрытия "
                        f"на данном шаге: \n{node}")

        if problem.goal_test(node.state):
            print("Решение найдено! Целевое состояние достигнуто.",
                  f"Время выполнения: {problem.count_new_states}",
                  f"Использование памяти: {Node.node_counter}", sep='\n')
            return node

        nodes = queuing_fn(nodes, problem.expand(node, node.operators))
        problem.message(
            "Кайма после раскрытия вершины:\n",
            '\n'.join([
                f"{node}\t"
                f"A*-estimation(h1 + g) = {h1(node.state) + node.depth}"
                for node in nodes
            ])
        )


def h1(state: tuple[tuple[int | str]]) -> int:
    """Количество не на своих местах цифр"""
    return sum(
        [
            1
            for line in zip(state, goal_state)
            for el1, el2 in zip(line[0], line[1])
            if el1 != el2
        ]
    )


def A_star(nodes: deque[Node], children: list[Node]) -> deque[Node]:
    nodes.extend(children)
    return deque(sorted(nodes, key=lambda node: h1(node.state) + node.depth))


def interactive_print(steps):
    choice = input("Выберите опцию вывода:\n1) Вывести все сразу\n2) "
                   "Выводить каждый шаг после нажатия Enter\nВаш выбор: ")
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


start_state = (
    (7, 4, 2),
    (3, 5, 8),
    (1, ' ', 6)
)
goal_state = (
    (1, 2, 3),
    (4, ' ', 5),
    (6, 7, 8)
)


while True:
    choise = input("Выберите опцию работы программы:\n"
                   "0) Вывести только результат\n1) Вывести всё сразу\n"
                   "2) Выводить каждый шаг после нажатия Enter\nВаш выбор: ")
    if choise == "0":
        mode = "silent"
    elif choise == "1":
        mode = "fast"
    elif choise == "2":
        mode = "step"
    else:
        print("Некорректный выбор. Попробуйте снова.")
        continue
    break

try:
    solution_node = general_search(Problem(start_state, goal_state, mode=mode),
                                   A_star)
    print_solution(solution_node)
except Exception as e:
    print(e)
