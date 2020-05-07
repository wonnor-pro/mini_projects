import random
import copy
import pygame

black_color = (0, 0, 0)
white_color = (255, 255, 255)
gray_color  = (150, 150, 150)
green_color = (169, 232, 122)
blue_color = (107, 131, 215)

class patterns:

    def __init__(self, lis):

        # Size of the board
        self.size = len(lis[0])

        # The pattern hint [[For columns], [For rows]]
        self.ls = copy.deepcopy(lis)

        # Show if conditions have been met
        self.state = [[0 for _ in range(self.size)] for _ in range(2)]

        # Store board status
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def draw(self, screen):

        '''
        Draw the percolation_system nxn board, top left
        corner is (40,40), each block is a 40px square.
        :param screen: pycham screen
        :return:
        '''
        for h in range(self.size+1):

            pygame.draw.line(screen, black_color,
                             (40 * 5, 40 * 5 + h * 40), (40 * 5 + self.size * 40, 40 * 5 + h * 40), 1)
            pygame.draw.line(screen, black_color,
                             (40 * 5 + h * 40, 40 * 5), (40 * 5 + h * 40, 40 * 5 + self.size * 40), 1)

        # Outside boundary
        pygame.draw.rect(screen, black_color, (40 * 5, 40 * 5, self.size * 40, self.size * 40), 3)

        pygame.display.flip()

    def show_board(self, screen):

        # Show the board
        for x in range(self.size):
            for y in range(self.size):
                color = [white_color, gray_color][self.board[x][y]]
                pygame.draw.rect(screen, color, (40 * 5+ y*40, 40 * 5+ x*40, 40, 40), 0)

        self.draw(screen)

    def clean_number(self, screen):

        # Clean all the numbers
        pygame.draw.rect(screen, white_color, (0, 0, 5 * 40 + self.size * 40, 5 * 40 - 5), 0)
        pygame.draw.rect(screen, white_color, (0, 0, 5 * 40 - 5, 5 * 40 + self.size * 40), 0)

    def show_number(self, screen):

        # Set the font
        font = pygame.font.SysFont("arialhbttc", 27)

        # For columns
        for i in range(self.size):
            ls = copy.deepcopy(self.ls[0][i])
            ls.reverse()
            for j in range(len(ls)):
                color = [black_color, blue_color][self.state[0][i]]
                text = font.render(f"{ls[j]}", True, color)
                screen.blit(text, (40 * 5 + 13 + i * 40, 40 * 4 + 8 - j * 40))

        # For rows
        for i in range(self.size):
            ls = copy.deepcopy(self.ls[1][i])
            ls.reverse()
            for j in range(len(ls)):
                color = [black_color, blue_color][self.state[1][i]]
                text = font.render(f"{ls[j]}", True, color)
                screen.blit(text, (40 * 4 + 13 - j * 40, 40 * 5 + 8 + i * 40))

    def mark_open(self, cursor_index):

        '''
        Use cursor to mark open (set that block to white)
        :param cursor_index: (y, x)
        :return:
        '''
        y, x = cursor_index
        board_range = (40 * 5, 40 * 5 + self.size * 40)

        if x < board_range[1] and x > board_range[0] and y < board_range[1] and y > board_range[0]:

            x = (x - 40 * 5) // 40
            y = (y - 40 * 5) // 40

            self.board[x][y] = not (self.board[x][y])
            self.update_state((x,y))

    def update_state(self, index):

        '''
        Use cursor to mark open (set that block to white)
        :param cursor_index: (y, x)
        :return:
        '''

        y, x = index

        self.state[0][x] = [0, 1][self.parse_line(x, Row=True) == self.ls[0][x]]
        self.state[1][y] = [0, 1][self.parse_line(y, Row=False) == self.ls[1][y]]

    def parse_line(self, number, Row = False):

        '''
        Given a line number, count continuous 1s and return its pattern in a list
        :param number: int
        :param Row: True: for rows; False: for columns
        :return: patterns in lists: e.g. [1,1,3]
        '''

        # Get the line
        if Row:
            line = [self.board[i][number] for i in range(self.size)]
        else:
            line = self.board[number]

        result = []
        count = 0

        for index, i in enumerate(line):

            # add one for count if its 1
            if i == 1:
                count += 1
                if index +1 == self.size:
                    result.append(count)

            # if it goes to 0, then append the count to
            # the list if count is greater than 0
            if i == 0 and count > 0:
                result.append(count)
                count = 0

        return result

    def reset(self):

        '''
        Turn all the blocks to white. And reset the states.
        :return:
        '''
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.state = [[0 for _ in range(self.size)] for _ in range(2)]

    def is_finished(self):

        # Check if the game is finished.
        for i in range(2):
            for status in self.state[i]:
                if status == False:
                    return False

        return True

    def finish(self, screen):

        # If finished, show congratulations on the screen
        if self.is_finished():

            font = pygame.font.SysFont("newyorkttf", 40)
            text = font.render(f"Congratulations!", True, blue_color)
            screen.blit(text, (5, 5))

def main():
    example = [[[7], [3, 3], [1, 1, 1], [3], [3, 1], [3, 2], [3], [5, 2], [4, 2], [4, 2]],
               [[1, 2], [3, 3], [3, 3], [3, 2, 3], [2, 1, 1, 1], [2], [1, 1], [2, 2], [2, 5], [3, 4]]]

    example2 = [[[5], [5], [3], [1], [2, 2, 1, 1], [2, 5], [2, 1, 3], [3, 4], [4], [1, 5]],
                [[2, 4], [3, 4, 1], [3, 1], [3], [2, 1], [3, 1], [1, 3], [7], [5], [6]]]

    # Initiate the object
    board = patterns(example2)
    size = len(example2[0])

    # Initialise the pygame
    pygame.init()
    pygame.display.set_caption('patterns')

    # Set the size of the window
    screen = pygame.display.set_mode((size*40 + 40 + 40 * 5, size*40 + 40 + 40 * 5))

    # Set background color
    screen.fill(white_color)

    # Draw essential parts on the screen
    board.show_board(screen)
    board.show_number(screen)
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

            # When click, draw the board
            if event.type == pygame.MOUSEBUTTONDOWN:

                board.mark_open(pygame.mouse.get_pos())
                board.clean_number(screen)
                board.show_board(screen)
                board.show_number(screen)
                board.finish(screen)
                pygame.display.flip()

            # When pressing space key, randomise the state anf show the board
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                pass
                # board.clean_number(screen)
                # pygame.display.flip()

            # When pressing c key, clean all the board
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:

                board.reset()
                board.clean_number(screen)
                board.show_board(screen)
                board.show_number(screen)
                pygame.display.flip()


    pygame.quit()


if __name__ == '__main__':
    main()