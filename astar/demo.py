import random
import copy
import pygame

black_color = (0, 0, 0)
white_color = (255, 255, 255)
green_color = (169, 232, 122)
blue_color = (137, 181, 215)
gray_color = (200, 200, 200)
red_color = (215, 96, 85)


def astar_key(state):
    return state.f


class state:

    def __init__(self, previous_state, new_index, initial, end):
        self.path = []
        self.path += previous_state + [new_index]
        self.node = new_index
        self.h = self.distance(self.node, end)
        self.g = self.distance(initial, self.node)
        self.f = self.h + self.g

    def __str__(self):
        output = ""
        for i in self.path:
            output += f"({i[0]},{i[1]}), "
        output += f"F = {self.f}"
        return output

    def distance(self, index_1, index_2):
        x_1, y_1 = index_1
        x_2, y_2 = index_2
        distance = ((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** 0.5
        # distance = abs(x_1 - x_2) + abs(y_1 - y_2)
        return distance


class map:

    def __init__(self, size, screen):
        self.screen = screen
        self.size = size
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # 0 for normal, 1 for block, 2 for initial, 3 for end, 4 for path
        self.status = 0
        self.initial = (0, 0)
        self.end = (size - 1, size - 1)
        # Store the path in another attribute
        self.path = copy.deepcopy(self.board)
        self.score = copy.deepcopy(self.board)

        self.frontier = []
        self.explored = []

    def __str__(self):
        output = "========== STATUS ===========\n"
        output += f"The begin point is {self.initial}, and the end point is {self.end}.\n"
        for i in self.path:
            for j in i:
                output += f"{j}"
            output += "\n"

        return output

    def draw(self):

        '''
        Draw the percolation_system nxn board, top left
        corner is (40,40), each block is a 40px square.
        :param screen: pycham screen
        :return:
        '''
        for h in range(self.size + 1):
            pygame.draw.line(self.screen, black_color,
                             (40, 40 + h * 40), (40 + self.size * 40, 40 + h * 40), 1)
            pygame.draw.line(self.screen, black_color,
                             (40 + h * 40, 40), (40 + h * 40, 40 + self.size * 40), 1)

        # Outside boundary
        pygame.draw.rect(self.screen, black_color, (40, 40, self.size * 40, self.size * 40), 3)

        pygame.display.flip()

    def show_text(self):

        pygame.draw.rect(self.screen, white_color, (self.size * 40 + 10, 20, 170, self.size * 40), 0)
        font = pygame.font.SysFont('freesansbold.ttf', 32)
        text = font.render('Status', True, black_color)
        self.screen.blit(text, (self.size * 40 + 60, 40))
        color = [white_color, black_color, blue_color, green_color, gray_color, red_color][self.status]
        status_text = ["Normal", "Block", "Initial", "End", "Solving", "Found"][self.status]
        text = font.render(status_text, True, color)
        self.screen.blit(text, (self.size * 40 + 60, 80))

    def show_state(self):

        self.show_text()

        for x in range(self.size):
            for y in range(self.size):
                # According to the label of each element, determine the color
                # 0 - not open (white)
                # 1 - open (black)
                # 2 - connected to the upper surface (blue)
                # 3 - connected to the both ends (green)
                color = [white_color, black_color, blue_color, green_color, gray_color, red_color][self.path[x][y]]
                pygame.draw.rect(self.screen, color, (40 + y * 40, 40 + x * 40, 40, 40), 0)

        self.draw()

    def mark_open(self, cursor_index):

        '''
        Use cursor to mark open (set that block to white)
        :param cursor_index: (y, x)
        :return:
        '''
        y, x = cursor_index
        board_range = (40, 40 + self.size * 40)

        if x < board_range[1] and x > board_range[0] and y < board_range[1] and y > board_range[0]:

            x = (x - 40) // 40
            y = (y - 40) // 40

            self.path[x][y] = self.status

            if self.status == 2:
                self.initial = (x, y)
                self.status = 1
            if self.status == 3:
                self.end = (x, y)
                self.status = 1

    def randomise(self):

        '''
        Randomly generate a state.
        :return:
        '''

        self.board = [[random.randint(0, 1) for _ in range(self.size)] for _ in range(self.size)]
        self.path = copy.deepcopy(self.board)

    def reset(self):

        '''
        Turn all the blocks to black (off).
        :return:
        '''
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.path = copy.deepcopy(self.board)
        self.frontier = []
        self.explored = []
        self.status = 0

    def find_next_state(self):
        if self.initial not in self.explored:
            initial_state = state([], self.initial, self.initial, self.end)
            return initial_state
        else:
            self.frontier.sort(key=astar_key)
            # for single_state in self.frontier:
            #     print(single_state)
            return self.frontier.pop(0)

    def explore_state(self, node_state):
        last_index = node_state.node
        candidate_index = [(last_index[0] + 1, last_index[1]),
                           (last_index[0] - 1, last_index[1]),
                           (last_index[0], last_index[1] + 1),
                           (last_index[0], last_index[1] - 1)]

        for index in candidate_index:
            if index not in self.explored and index[0] >= 0 and index[1] >= 0 and index[0] <= self.size and index[
                1] <= self.size:
                if self.path[index[0]][index[1]] != 1:
                    self.frontier.append(state(node_state.path, index, self.initial, self.end))

        self.explored.append(last_index)
        i = last_index
        self.path[i[0]][i[1]] = 4
        self.show_state()
        pygame.display.flip()

    def solve(self):
        self.status = 4
        node_state = None
        while self.end not in self.explored:
            node_state = self.find_next_state()
            self.explore_state(node_state)

        self.status = 5
        print(self.explored)

        return node_state


def main():
    size = 20

    # Initialise the pygame
    pygame.init()
    pygame.display.set_caption('a-star')

    # Set the size of the window
    screen = pygame.display.set_mode((size * 40 + 80 + 100, size * 40 + 80))

    # Set background color
    screen.fill(white_color)

    # Initiate the object
    board = map(size, screen)

    # Draw essential parts on the screen
    board.show_state()
    pygame.display.flip()

    # Set the progress flag
    done = False

    while not done:

        for event in pygame.event.get():

            # Exit key
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

            # When click, draw the path
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.mark_open(pygame.mouse.get_pos())
                board.show_state()
                pygame.display.flip()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                board.status = 0
                board.show_state()
                pygame.display.flip()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                board.status = 1
                board.show_state()
                pygame.display.flip()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                board.status = 2
                board.show_state()
                pygame.display.flip()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                board.status = 3
                board.show_state()
                pygame.display.flip()

            # When pressing space key, randomise the state anf show the path
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print(board)
                result = board.solve()
                print(result)
                for i in result.path:
                    board.path[i[0]][i[1]] = 5
                board.path[board.initial[0]][board.initial[1]] = 2
                board.path[board.end[0]][board.end[1]] = 3
                board.show_state()
                pygame.display.flip()

            # When pressing c key, clean all the path
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                board.reset()
                board.show_state()
                pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
