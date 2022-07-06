# Gitali Naim and Avital Abergel

import sys
from random import randint, random
import time

# number of rows and columns in each matrix
size = 25
# total number of matrices in each generation
amount = 100


# convert the matrix to binary numbers in a list
def mat_to_bin(mat):
    binary = []
    for row in mat:
        for sqr in row:
            binary.append(sqr)
    return binary


# convert a list of binary numbers to matrix
def bin_to_mat(binary):
    mat = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(binary[size * i + j])
        mat.append(row)
    return mat


# print the board of the matrix
def print_board(binary_board):
    mat = []
    # initialize the matrix with the sign □ that represent 0
    for i in range(size):
        board_row = []
        for j in range(size):
            board_row.append("□")
        mat.append(board_row)
    # the sign ■ represent 1
    for x in range(size):
        for y in range(size):
            if binary_board[x][y] == 1:
                mat[x][y] = "■"

    # print the board of the matrix
    for line in mat:
        for item in line:
            print(item, end="  ")
        print()


# count the number of black blocks in a row or column in the matrix
def block_counter(vec):
    last = 0
    counter = 0
    # pass over each cell in the vector
    for sqr in vec:
        if sqr != last:
            counter += 1 - last
            last = 1 - last
    return counter


# count the number of black cells in each block
# get a vector of row or column and return a list
def block_divider(vec):
    counter = 0
    return_lst = []
    # pass over each cell in the vector
    for sqr in vec:
        if sqr == 1:
            counter += 1
        elif counter != 0:
            return_lst.append(counter)
            counter = 0
    if counter != 0:
        return_lst.append(counter)
    return return_lst


# evaluation matrix - fitness
def fitness(rows, cols_cons, rows_cons):
    # create a new matrix that represent the columns
    cols = []
    for x in range(size):
        col = []
        for y in range(size):
            col.append(rows[y][x])
        cols.append(col)

    score = 0
    lst_col_tuples = []
    lst_row_tuples = []

    # pass over the two matrices - first that represent the columns and second the rows
    for i in range(size):
        col_tuples = []
        row_tuples = []
        col_blocks_list = block_divider(cols[i])
        row_blocks_list = block_divider(rows[i])

        # match for any constraint a block (the number of black cells in it)
        for j in range(len(col_blocks_list)):
            tup = (int(col_blocks_list[j]), int(cols_cons[i][j]))
            col_tuples.append(tup)

        for j in range(len(row_blocks_list)):
            tup = (int(row_blocks_list[j]), int(rows_cons[i][j]))
            row_tuples.append(tup)

        # for constraints for which there is no match block - we will write the number 0
        for j in range(len(col_blocks_list), len(cols_cons[i])):
            tup = (0, int(cols_cons[i][j]))
            col_tuples.append(tup)
        lst_col_tuples.append(col_tuples)

        for j in range(len(row_blocks_list), len(rows_cons[i])):
            tup = (0, int(rows_cons[i][j]))
            row_tuples.append(tup)
        lst_row_tuples.append(row_tuples)

    # initialize two counters
    counter1 = 0
    counter2 = 0

    # calculate the fitness for each tuple
    for lst in lst_col_tuples:
        for tup in lst:
            if max(tup[0], tup[1]) > 0:
                score += abs(tup[0] - tup[1]) / max(tup[0], tup[1])
            if tup[0] != 0 and tup[1] != 0:
                counter2 += 1
                if tup[0] == tup[1]:
                    counter1 += 1

    for lst in lst_row_tuples:
        for tup in lst:
            if max(tup[0], tup[1]) > 0:
                score += abs(tup[0] - tup[1])/max(tup[0], tup[1])
            if tup[0] != 0 and tup[1] != 0:
                counter2 += 1
                if tup[0] == tup[1]:
                    counter1 += 1
    counter = counter1 / counter2
    return score, counter


# crossover function - get two matrices and return new matrix
def crossover(mat1, mat2):
    bin1, bin2 = mat_to_bin(mat1), mat_to_bin(mat2)
    ret_bin = []
    # generate a random index
    cut = randint(1, size ** 2 - 2)
    # the random index is dividing the binary sequences into 2 halves
    # the new binary sequence is half from the first one and half from the other one
    for i in range(cut):
        ret_bin.append(bin1[i])
    for i in range(cut, size ** 2):
        ret_bin.append(bin2[i])
    ret_mat = bin_to_mat(ret_bin)
    return ret_mat


# mutation function - return new matrix after mutation
def mutation(matrix):
    binary = mat_to_bin(matrix)
    # generate a random index
    rand_idx = randint(0, size**2 - 1)
    # change the value in the chosen index
    binary[rand_idx] = 1 - binary[rand_idx]
    matrix = bin_to_mat(binary)
    return matrix


# create the new generation
def generations(gen, cols_cons, rows_cons, algo_type):
    return_gen = []
    gen_fit = []
    if algo_type == "Normal":
        for i in range(0, amount):
            gen_fit.append(fitness(gen[i], cols_cons, rows_cons)[0])
    if algo_type == "Darwin":
        for i in range(0, amount):
            gen_fit.append(fitness(optimization(gen[i]), cols_cons, rows_cons)[0])
    if algo_type == "Lamarck":
        for i in range(0, amount):
            opt_gen = optimization(gen[i])
            if fitness(opt_gen, cols_cons, rows_cons) < fitness(gen[i], cols_cons, rows_cons):
                gen[i] = opt_gen
            gen_fit.append(fitness(gen[i], cols_cons, rows_cons)[0])

    gen_list = []
    # append to new list the fitness value and its matrix
    for i in range(0, amount):
        gen_list.append([gen_fit[i], gen[i]])

    # sort the list according to the fitness
    sorted_gen_list = sorted(gen_list)
    sorted_gen = []
    for i in range(amount):
        sorted_gen.append(sorted_gen_list[i][1])

    # replication of the 2 best matrices 5 times
    for i in range(2):
        for j in range(5):
            return_gen.append(sorted_gen[i])

    # make crossover on 90 matrices
    for i in range(amount - 10):
        rand1 = randint(0, amount - 1)
        rand2 = randint(0, amount - 1)
        return_gen.append(crossover(sorted_gen[rand1], sorted_gen[rand2]))

    # make mutation on each matrix in probability of 0.15
    for i in range(amount):
        chance = random()
        if chance < 0.15:
            return_gen[i] = mutation(return_gen[i])
    return return_gen


# optimization matrix for Darwin and Lamarck algorithm
def optimization(mat):
    binary = mat_to_bin(mat)
    for i in range(50):
        rand1 = randint(0, size ** 2 - 1)
        rand2 = randint(0, size ** 2 - 1)
        binary[rand1], binary[rand2] = binary[rand2], binary[rand1]
    mat = bin_to_mat(binary)
    return mat


def main():
    # read the input data and split it to columns cons and rows cons
    with open(sys.argv[1], "r") as txt_input:
        txt_list = [(line.rstrip()) for line in txt_input]
        for i in range(len(txt_list)):
            line = txt_list[i].replace(" ", "")
            line = line[::-1].zfill(13)
            line = line[::-1]
            txt_list[i] = line
    col_input, row_input = [], []
    for i in range(25):
        col_input.append(txt_list[i])
        row_input.append(txt_list[i + 25])

    # create the first generation of the matrices
    matrices = []
    for i in range(amount):
        matrix = []
        for j in range(size):
            row = []
            for k in range(size):
                row.append(randint(0, 1))
            matrix.append(row)
        matrices.append(matrix)

    # get input from the user
    print("Normal, Darwin, Lamarck")
    algo = input()
    # run 1500 generations
    for i in range(1500):
        matrices = generations(matrices, col_input, row_input, algo)

    minimum = 9999
    min_mat = []
    max_counter = 0

    # find the lowest fitness
    for matrix in matrices:
        fit, counter = fitness(matrix, col_input, row_input)
        if fit < minimum:
            max_counter = counter
            minimum = fit
            min_mat = matrix
    max_counter = int(max_counter * 100)
    print(str(max_counter) + "%")
    print(minimum)
    print_board(min_mat)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
