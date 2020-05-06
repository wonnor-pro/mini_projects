import random
import copy
import pygame

black_color = (0, 0, 0)
white_color = (255, 255, 255)
green_color = (169, 232, 122)
blue_color = (137, 181, 215)

class percolation_system:

    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.path = copy.deepcopy(self.board)

    def draw(self, screen):

        '''
        Draw the percolation_system nxn board, top left
        corner is (40,40), each block is a 40px square.
        :param screen: pycham screen
        :return:
        '''
        for h in range(self.size+1):

            pygame.draw.line(screen, black_color,
                             (40, 40 + h * 40), (40 + self.size * 40, 40 + h * 40), 1)
            pygame.draw.line(screen, black_color,
                             (40 + h * 40, 40), (40 + h * 40, 40 + self.size * 40), 1)

        pygame.draw.rect(screen, black_color, (40, 40, self.size * 40, self.size * 40), 3)

        pygame.display.flip()

    def clean_board(self, screen):

        pygame.draw.rect(screen, white_color, (40, 40, self.size * 40, self.size * 40), 0)
        self.draw(screen)

    def show_state(self, screen):

        for x in range(self.size):
            for y in range(self.size):
                color = [black_color, white_color, blue_color, green_color][self.path[x][y]]
                pygame.draw.rect(screen, color, (40 + y*40, 40 + x*40, 40, 40), 0)

        self.draw(screen)

    def node(self, index, back = False):
        x, y = index

        status_open = 1
        status_got = 2
        status_succeed = 3

        i, j = status_open, status_got
        if back:
            i, j = status_got, status_succeed

        first_row    = (x == 0)
        first_column = (y == 0)
        last_row     = (x + 1 == self.size)
        last_column  = (y + 1 == self.size)

        if not first_row:
            if self.path[x-1][y] == i or (back and self.path[x-1][y] == status_open):
                self.path[x - 1][y] = j
                self.node((x-1, y), back)

        if not last_row:
            if self.path[x+1][y] == i or (back and self.path[x+1][y] == status_open):
                self.path[x + 1][y] = j
                self.node((x+1, y), back)

        if not first_column:
            if self.path[x][y-1] == i or (back and self.path[x][y-1] == status_open):
                self.path[x][y - 1] = j
                self.node((x, y-1), back)

        if not last_column:
            if self.path[x][y+1] == i or (back and self.path[x][y+1] == status_open):
                self.path[x][y+1] = j
                self.node((x, y+1), back)


    def solve_path(self):

        for i in range(self.size):
            if self.path[0][i] == 1:
                self.path[0][i] = 2

        for x in range(self.size):
            for y in range(self.size):
                if self.path[x][y] == 2:
                    self.node((x, y))

        for i in range(self.size):
            if self.path[-1][i] == 2:
                self.path[-1][i] = 3

        for x in range(self.size):
            for y in range(self.size):
                if self.path[x][y] == 3:
                    self.node((x, y), back=True)

    def mark_open(self, cursor_index):

        y, x = cursor_index
        board_range = (40, 40 + self.size * 40)

        if x < board_range[1] and x > board_range[0] and y < board_range[1] and y > board_range[0]:

            x = (x - 40) // 40
            y = (y - 40) // 40

            self.path[x][y] = 1
            self.solve_path()

    def randomise(self):

        self.board = [[random.randint(0, 1) for _ in range(self.size)] for _ in range(self.size)]
        self.path = copy.deepcopy(self.board)

    def clean(self):

        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.path = copy.deepcopy(self.board)

def main():

    size = 20

    # Initiate the object
    board = percolation_system(size)

    # Initialise the pygame
    pygame.init()
    pygame.display.set_caption('percolation')

    # Set the size of the window
    screen = pygame.display.set_mode((size*40 + 80, size*40 + 80))

    # Set background color
    screen.fill(white_color)

    # Draw essential parts on the screen
    board.show_state(screen)
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
                board.show_state(screen)
                pygame.display.flip()

            # When pressing space key, randomise the state anf show the path
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                board.randomise()
                board.solve_path()
                board.show_state(screen)
                pygame.display.flip()

            # When pressing c key, clean all the path
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:

                board.clean()
                board.show_state(screen)
                pygame.display.flip()


    pygame.quit()


if __name__ == '__main__':
    main()