import random
import pygame
import time
import matplotlib.pyplot as plt
import numpy as np

black_color = (0, 0, 0)
white_color = (255, 255, 255)
green_color = (169, 232, 122)
blue_color = (137, 181, 215)
gray_color = (128,128,128)
red_color = (255, 100, 0)
world_size = 640

class creature:

    def __init__(self, energy = 500, scale=5, legacy=-1) :
        self.location = (random.gauss(world_size // 2, 2) // 1, (random.gauss(world_size // 2, 2) // 1))
        self.world_size = world_size
        self.scale = scale
        if legacy == -1:
            self.kind = random.randint(0,2)
        else:
            kinds = [legacy for _ in range(5)] + [0,1,2]
            self.kind = kinds[random.randint(0,len(kinds)-1)]
        self.step = [5, 10, 15][self.kind]
        self.energy = energy
        self.age = 0

    def move(self):
        if self.energy > 0:
            self.age += 1
            movement = [(1, 0), (-1, 0), (1, 1), (-1, -1), (0, 1), (0, -1), (1, -1), (-1, 1)][random.randint(0, 7)]
            scale_x = random.gauss(self.step, 2) // 1
            scale_y = random.gauss(self.step, 2) // 1
            print(self.kind, scale_x, scale_y)

            move_x = min(self.location[0] + scale_x * movement[0], self.world_size - self.scale)
            move_y = min(self.location[1] + scale_y * movement[1], self.world_size - self.scale)
            move_x = max(move_x, self.scale)
            move_y = max(move_y, self.scale)

            self.location = (move_x, move_y)

            self.energy -= (self.scale * self.scale * self.scale * (scale_x **2 + scale_y **2))**0.2 // 1
            print((self.scale * self.scale * self.scale * (scale_x **2 + scale_y **2))**0.2 // 1)

    def eat(self):
        self.energy += 250

        if self.scale <= 14:
            self.scale += 1

class world:

    def __init__(self, world_size, initial_creature=10):
        self.world_size = world_size
        self.initial_creature = initial_creature
        self.creature = [creature() for _ in range(self.initial_creature)]
        self.food = [((random.gauss(world_size // 2, 200)) // 1, (random.gauss(world_size // 2, 200)) // 1) for _ in range(100)]
        self.days = 0
        self.records = []

    def show(self, screen):
        self.clear(screen)
        self.show_food(screen)
        self.show_creature(screen)

        pygame.display.flip()

    def show_food(self, screen):
        for location in self.food:
            pygame.draw.circle(screen, gray_color, location, 2, 0)

    def show_creature(self, screen):
        for single_creature in self.creature:
            color = [green_color, blue_color, red_color][single_creature.kind]
            pygame.draw.circle(screen, color, single_creature.location, single_creature.scale, 0)

    def clear(self, screen):
        pygame.draw.rect(screen, white_color, (0, 0, self.world_size, self.world_size), 0)

    def update(self):
        new = []
        self.days += 1

        if self.days%100 == 0:
            new_food = [((random.gauss(world_size // 2, 100)) // 1, (random.gauss(world_size // 2, 100)) // 1) for _ in range(20)]
            self.food += new_food
        for creature_index, single_creature in enumerate(self.creature):
            print((single_creature.scale, single_creature.energy, single_creature.age))
            if single_creature.energy <= 0:
                self.creature.pop(creature_index)
            else:
                single_creature.move()
                for index, food in enumerate(self.food):
                    if ((single_creature.location[0]-food[0])**2 + (single_creature.location[1]-food[1])**2 ) <= single_creature.scale**2:
                        single_creature.eat()
                        print(self.food.pop(index))
                        if single_creature.energy >= 400 and single_creature.scale >= 8 and single_creature.age > 100:
                            single_creature.energy //= 2
                            single_creature.scale //= 2
                            new.append(single_creature.kind)
        for kind in (new):
            self.creature.append(creature(legacy=kind))

        kind = [0,0,0]

        for i in self.creature:
            kind[i.kind] += 1
        if self.days%10 == 0:
            self.records.append((self.days, sum(kind), len(self.food), kind[0], kind[1], kind[2]))

def main():

    # Initiate the object
    world_simulation = world(world_size, initial_creature=10)

    # Initialise the pygame
    pygame.init()
    pygame.display.set_caption('World simulation')

    # Set the size of the window
    screen = pygame.display.set_mode((world_size, world_size))

    # Set background color
    screen.fill(white_color)

    # Draw essential parts on the screen
    world_simulation.show(screen)

    # Set the progress flag
    done = False
    Analysis = False

    while not done:

        if not Analysis:

            world_simulation.update()
            world_simulation.show(screen)
            time.sleep(0.05)

        for event in pygame.event.get():

            # Exit key
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

            # When pressing space key, randomise the state anf show the path
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Analysis = True
                data = np.array(world_simulation.records)
                print(data[0])
                print(data.shape)
                days = data[:,0]
                amount_of_creatures = data[:,1]
                amount_of_food = data[:, 2]

                plt.subplot(211)
                plt.plot(days, amount_of_creatures, label="Total")
                plt.plot(days, data[:, 3], label="slow")
                plt.plot(days, data[:, 4], label="normal")
                plt.plot(days, data[:, 5], label="fast")
                plt.legend()
                plt.subplot(212)
                plt.plot(days, amount_of_food)
                plt.suptitle('World Analysis')
                plt.show()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                Analysis = False


    pygame.quit()


if __name__ == '__main__':
    main()