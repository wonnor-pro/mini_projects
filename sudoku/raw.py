import numpy as np

class state:

    def __init__(self, input_state):
        self.initial = input_state
        self.lis = self.initial
        self.array = np.array(self.lis)
        self.unknowns = 81
        self.solvable = True
        self.candidate = [[0 for i in range(9)] for j in range(9)]
        self.update()

    def __str__(self):

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
        unknowns = sum([i.count(0) for i in self.lis])
        self.unknowns = unknowns
        return unknowns

    def get_block_list(self, index):
        x = index[0]
        y = index[1]

        top_left_index = (x // 3 * 3, y // 3 * 3)
        block_list = []
        for i in range(3):
            for j in range(3):
                block_list.append(self.lis[top_left_index[0] + i][top_left_index[1] + j])
        return block_list

    def verify(self, index, number):

        if number in self.get_candidate(index):
            return True

        return False

    def get_candidate(self, index):

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
                    self.candidate[x][y] = -1
        return True

    def update(self):
        self.array = np.array(self.lis)
        self.update_unknown_numbers()
        self.update_candidate_map()

    def solve(self):

        if self.unknowns == 0:
            print(self)
            return self.lis

        for i in range(9):
            for j in range(9):

                if self.candidate[i][j] == 0:
                    continue
                else:
                    min_set = self.get_candidate((i,j))

                    for possibility in min_set:

                        ls = self.lis
                        ls[i][j] = possibility

                        new_state = state(ls)
                        solution = new_state.solve()

                        if solution:
                            self.lis = solution
                            return solution

                        ls[i][j] = possibility

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

if __name__ == '__main__':
    main()