import pygame
import numpy as np
import time
import random
print(pygame.ver)

black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 0, 0)

class queens:

    def __init__(self, number):
        self.lis = []
        self.queens = number
        self.heuristic = [[0 for i in range(number)] for j in range(number)]
        self.solved = False

        # randomise the position of each queens
        self.randomise()
        # Update the unknowns and candidate map
        self.update()

    def randomise(self):

        # Randomly generate the queens position in each column to kick off
        self.lis = [random.randint(1, self.queens - 1) for i in range(self.queens)]

    def draw(self, screen):

        '''
        Draw the queens nxn board, top left cornor is (40,40),
        each block is a 40px square.
        :param screen: pycham screen
        :return:
        '''
        for h in range(self.queens+1):

            pygame.draw.line(screen, black_color,
                             (40, 40 + h * 40), (40 + self.queens * 40, 40 + h * 40), 1)
            pygame.draw.line(screen, black_color,
                             (40 + h * 40, 40), (40 + h * 40, 40 + self.queens * 40), 1)

        pygame.draw.rect(screen, black_color, (40, 40, self.queens * 40, self.queens * 40), 3)

    def show_single(self, color, index, screen):

        '''
        To show single queen
        :param color: RGB
        :param index: (x, y): note x means column
        :param screen: pygame screen
        :return:
        '''
        # Set the font
        font = pygame.font.SysFont("bodoniornamentsttf", 20)

        # As in self.lis, the first index means rows
        y, x = index

        text = font.render("k", True, color)
        screen.blit(text, (50 + y * 40, 50 + x * 40))

        pygame.display.flip()

    def show_state(self, color, screen):

        '''
        Display the digit on specific position
        :param color: RGB color in tuple
        :param screen: pygame screen
        :return:
        '''

        # Set the font
        font = pygame.font.SysFont("bodoniornamentsttf", 20)

        # As in enumerate, the first index means rows
        for y,x in enumerate(self.lis):
            text = font.render("k", True, color)
            screen.blit(text, (50 + y * 40, 50 + x * 40))

        pygame.display.flip()

    def show_digit(self, index, color, screen):

        '''
        Display the digit on specific position
        :param index: (x,y)
        :param color: RGB color in tuple
        :param screen: pygame screen
        :return:
        '''

        # Set the font
        font = pygame.font.SysFont("arialhbttc", 12)

        # Get the digit
        x = index[0]
        y = index[1]
        digit = self.heuristic[x][y]

        # Id its non-zero, display the digit
        if digit != 0:
            text = font.render(f"{digit}", True, color)
            screen.blit(text, (45 + y * 40, 45 + x * 40))

    def show_all_digit(self, color, screen):

        for x in range(self.queens):
            for y in range(self.queens):
                self.show_digit((x,y), color, screen)

    def clean_digit(self, index, screen):
        y, x = index
        pygame.draw.rect(screen, white_color, (43 + y * 40, 43 + x * 40, 35, 35), 0)

    def clean_board(self, screen):

        '''
        clean all the content from the screen
        :param index: (x,y)
        :param screen: pygame screen
        :return:
        '''

        for x in range(self.queens):
            for y in range(self.queens):
                pygame.draw.rect(screen, white_color, (43 + y * 40, 43 + x * 40, 35, 35), 0)

        pygame.display.flip()

    def find_h(self, index):

        '''
        find the heuristic for single position
        :param index: (x, y) note that x means columns
        :return: h: integer heuristic for that position
                (global conflicts)
        '''
        x, y = index

        # store each points in the list
        ls = [index]
        for col, row in enumerate(self.lis):
            # Besides the current column, as we calculate the
            # conflicts if move the queen in that column to
            # the index position
            if col != x:
                ls.append((col, row))

        # Calculate conflicts with each pairs (combination)
        h = 0
        for i in range(len(ls)):
            for j in range(i,len(ls)):
                if self.is_against(ls[i], ls[j]):
                    h += 1

        return h

    def is_against(self, index1, index2):

        x1, y1 = index1
        x2, y2 = index2

        # Same column (this scenario generally will not happen)
        if x1 == x2:
            return False

        # Same row
        if y1 == y2:
            return True

        # Upper diagonal
        if abs(y2-y1) == abs(x2-x1):
            return True

        return False

    def update(self):

        # Find the heuristic for each position
        for x in range(self.queens):
            for y in range(self.queens):
                self.heuristic[x][y] = self.find_h((y,x))

    def find_entry(self):

        '''
        Find the entry with least heuristic to start trial
        :return: min_index: (x,y);
                 min_mount: number of least h for that position;
        '''

        min_index = (-1, -1)
        min_amount = 100

        for x in range(self.queens):
            for y in range(self.queens):
                if self.heuristic[x][y] < min_amount:
                    min_index = (y,x)
                    min_amount = self.heuristic[x][y]

        return min_index, min_amount

    def next(self, screen):

        '''
        Go to next stage
        :param screen: pygame screen
        :return:
        '''

        min_index, min_amount = self.find_entry()


        # If 0 heuristic exists, the solution has been found
        if min_amount == 0:
            self.solved = True

        # If not, according to the min_index move the queen
        x, y = min_index

        # Reset the content on the screen
        self.clean_board(screen)

        # Change the position
        self.lis[x] = y

        # Calculate the h for all blocks and show queens and heuristics
        self.update()
        self.show_state(black_color, screen)
        self.show_all_digit(black_color, screen)

        # Display
        pygame.display.flip()

    def solve(self, screen):

        '''
        Keep finding solution until get a solution
        :param screen:
        :return:
        '''

        while self.solved == False:

            # For each start point, with limited moves
            # we either find a solution or go to a dead end

            for _ in range(self.queens//2):
                self.next(screen)
                if self.solved:
                    break

            # If this trial fails, randomise the position
            # and update h map, go to next trail
            self.randomise()
            self.update()


def main():

    QUEEN = 8

    # Initiate the object
    board = queens(QUEEN)

    # Initialise the pygame
    pygame.init()
    pygame.display.set_caption('queens')

    # Set the size of the window
    screen = pygame.display.set_mode((QUEEN*40 + 80, QUEEN*40 + 80))

    # Set background color
    screen.fill(white_color)

    # Draw essential parts on the screen
    board.draw(screen)
    board.show_state(black_color, screen)
    board.show_all_digit(black_color, screen)
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

            # When click, start to solve
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.solve(screen)


    pygame.quit()


if __name__ == '__main__':
    main()
