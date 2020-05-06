import numpy as np

step = []
class state:

    def __init__(self, input_state):

        self.lis = input_state
        self.array = np.array(self.lis)
        self.unknowns = 81

        # Candidate map, the amount of candidates for each block are marked
        self.candidate = [[0 for i in range(9)] for j in range(9)]

        # Update the unknowns and candidate map
        self.update()

    def __str__(self):

        # Define the printing format of the state

        output = " ====== STATE ======  ==== CANDIDATE ====\n"
        for row in range(9):
            output += "|"
            for number in self.lis[row]:
                if number == 0:
                    output += " _"
                else:
                    output += f" {number}"
            output += (" |")
            output += "|"
            for number in self.candidate[row]:
                if number == -1:
                    output += " _"
                else:
                    output += f" {number}"
            output += (" |\n")

        output += ("========================================== \n")
        output += (f"It has {self.unknowns} unknown numbers.")
        return output

    def update_unknown_numbers(self):

        '''
        Count the unknown numbers for the state
        :return: amount of unknowns
        '''
        unknowns = sum([i.count(0) for i in self.lis])
        self.unknowns = unknowns
        return unknowns

    def get_block_list(self, index):

        '''
        Returns a list of numbers already filled in the
        3x3 block.
        :param index: (x,y)
        :return: list of nine [0~9] digits
        '''

        x = index[0]
        y = index[1]

        top_left_index = (x // 3 * 3, y // 3 * 3)
        block_list = []
        for i in range(3):
            for j in range(3):
                block_list.append(self.lis[top_left_index[0] + i][top_left_index[1] + j])
        return block_list

    def verify(self, index, number):
        '''
        To verify if a certain number can be sub into a
        certain position.
        :param index: (x,y)
        :param number: int
        :return: True/False
        '''
        if number in self.get_candidate(index):
            return True

        return False

    def get_candidate(self, index):
        '''
        Provide the candidate list for a certain position
        (x,y)
        :param index: (x,y)
        :return: set of candidates {1~9}
        '''

        full_list = {1,2,3,4,5,6,7,8,9}

        row = list(self.array[index[0], :])
        column = list(self.array[:, index[1]])
        block = self.get_block_list(index)

        all_numbers = set(row + column + block)

        return(full_list - all_numbers)

    def update_candidate_map(self):
        for x in range(9):
            for y in range(9):
                index = (x,y)
                if self.lis[x][y] == 0:
                    self.candidate[x][y] = len(self.get_candidate(index))
                else:
                    # The candidate map sets -1 to unknown position
                    self.candidate[x][y] = -1
        return True

    def update(self):

        # Update the state information from self.lis
        self.array = np.array(self.lis)
        self.update_unknown_numbers()
        self.update_candidate_map()
        # print(self)

    def find_entry(self):
        '''
        Find the entry with least candidate numbers to start
         trial
        :return: min_index: (x,y);
                 min_mount: number of least candidate numbers
                            for that position;
        '''

        min_index = (-1,-1)
        min_amount = 10

        for x in range(9):
            for y in range(9):

                # The candidate map sets -1 to unknown position
                if self.candidate[x][y] != -1 and self.candidate[x][y] < min_amount:
                    min_amount = self.candidate[x][y]
                    min_index = (x,y)

        return min_index, min_amount

    def solve(self):

        '''

        The solution uses backtrack algorithm to find a solution.
        It will try one possibility and enter next stage to solve
        it. If one candidate position gives 0 candidate then it
        returns False to upper lever, otherwise the solution will
        be returned.

        :return: Solution in list, or False
        '''

        # if all unknowns have been solved, the return the
        # solution.
        if self.unknowns == 0:
            print(self)
            return self.lis

        # if not, find the least candidate entry to start trial
        min_index, _ = self.find_entry()
        min_set = self.get_candidate(min_index)

        for possibility in min_set:

            # for each possible candidate, set the state
            self.lis[min_index[0]][min_index[1]] = possibility

            # pass it to next state and solve that state
            new_state = state(self.lis)
            solution = new_state.solve()

            # if a solution is received, then add that into the
            # step and return
            if solution:
                step.append([(min_index), possibility])
                return solution

            # if it fails to find the solution, set the position
            # back to 0 and go to next trial
            self.lis[min_index[0]][min_index[1]] = 0

        # if all trails fail, then return False as it is a dead
        # end
        return False

def main():
    easy = [[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]

    difficult = [[0,0,3,0,0,0,0,0,4],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,1,0,6,0],
                 [0,2,0,0,0,0,0,0,0],
                 [0,0,0,8,0,0,0,0,7],
                 [5,1,0,0,0,0,0,9,0],
                 [4,0,0,3,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,9,4,0,0,0,0,0]]

    difficult2 = [[0,0,5,2,8,0,0,0,0],
                  [0,0,0,0,0,4,1,0,0],
                  [0,0,9,0,0,0,4,0,3],
                  [9,0,0,7,0,0,0,6,0],
                  [0,8,0,0,1,0,0,4,0],
                  [0,5,0,0,0,9,0,0,1],
                  [4,0,6,0,0,0,2,0,0],
                  [0,0,7,4,0,0,0,0,0],
                  [0,0,0,0,2,5,6,0,0]]

    difficult3 = [[0,0,9,0,0,0,0,0,8],
                  [0,0,0,0,0,0,0,0,0],
                  [2,0,0,5,3,0,0,0,0],
                  [7,0,0,0,4,1,0,0,0],
                  [0,0,0,0,0,0,0,2,0],
                  [0,6,0,0,0,0,3,5,0],
                  [0,3,0,0,0,0,0,0,0],
                  [0,0,6,0,0,9,0,0,0],
                  [0,0,0,0,0,7,0,0,4]]

    state_0 = state(difficult3)
    print(state_0)
    print(state_0.solve())
    step.reverse()

    for each_step in step:
        print(f"Fill in {each_step[0]} with {each_step[1]}.")
    # print(step)1

    print(difficult3)


if __name__ == '__main__':
    main()