import sys
import copy
from random import randint

# Open the input file
with open(sys.argv[1], "r") as txt_input:
    txt_list = [(line.rstrip()) for line in txt_input]


# This function get a list of lists and convert it to one list
def mat_to_bin(mat):
    lst = []
    for row in mat:
        for cell in row:
            lst.append(int(cell))
    return lst

# only for question 4
def inputLstUpdate(inputLst, numOfDigits):
    for i in range(0,numOfDigits):
        for j in range(0, 99):
            if inputLst[i][j] == 0:
                inputLst[i][j] = -1
    return inputLst


# This function gets a number of digits we want to learn, and return a matrix in which each row represent a digit
def input_to_matrix(numOfDigits):
    inputLst = []
    for i in range(0, 110 * numOfDigits, 110):
        matrix = []
        for j in range(10):
            if txt_list[i + j] != '':
                matrix.append(txt_list[i + j])
            else:
                break
        inputLst.append(mat_to_bin(matrix))
    return inputLst


# This function get a matrix and calculate the weighted matrix
def weighted_matrix_func(inputLst):
    row_len = len(inputLst)
    col_len = len(inputLst[0])
    new_mat = []
    for i in range(col_len):
        row = []
        for j in range(col_len):
            row.append(0)
        new_mat.append(row)
    cols = []
    for x in range(col_len):
        col = []
        for y in range(row_len):
            col.append(inputLst[y][x])
        cols.append(col)

    for i in range(col_len):
        for j in range(col_len):
            counter = 0
            for x in range(row_len):
                if cols[i][x] == cols[j][x]:
                    counter += 1
                else:
                    counter -= 1
            new_mat[i][j] = counter
    return new_mat


# This function get a digit and change randomly 10% of the bits
def random_change(digit):
    new_digit = []
    for i in range(100):
        new_digit.append(0)

    copyDigit = copy.copy(digit)
    counter = 0
    while counter != 10:
        rand_idx = randint(0, 99)
        if new_digit[rand_idx] == 0:
            counter += 1
            new_digit[rand_idx] = 1

    for i in range(100):
        copyDigit[i] ^= new_digit[i]

    return copyDigit


# This function get a digit that has been changed in 10% of the bits, and try to reconstruct it
def reconstruction_func(randomDigit, weightedMatrix):
    prevS = copy.copy(randomDigit)
    while True:
        newS = copy.copy(prevS)
        prevS = []
        for i in range(len(randomDigit)):
            s = 0
            for j in range(len(randomDigit)):
                if i != j:
                    s += newS[j] * weightedMatrix[i][j]
            if s < 0:
                prevS.append(0)
            else:
                prevS.append(1)
        if newS == prevS:
            break
    return newS


# This function calculate the difference between 2 lists (2 digit)
def calculate_diffrence(inputList, digitAfterReconstuction):
    diffDict = {}
    for digit in range(len(inputList)):
        diff = 0
        for char in range(len(digitAfterReconstuction)):
            if inputList[digit][char] == digitAfterReconstuction[char]:
                diff += 1
        diffDict[digit] = diff
    diffValue = max(diffDict.values())
    diffValue = (diffValue / len(digitAfterReconstuction)) * 100
    diffIndex = [k for k, v in diffDict.items() if v == diffValue][0]
    return diffValue, diffIndex


# This function calculate the differences between all digits.
def list_of_diffrences(numOfDigits, inputLst, numOfChecks, weightedMatrix):
    allData = []
    for digit in range(numOfDigits):
        digitLst = []
        for i in range(numOfChecks):
            currentData = []  # Current data hold the data for the cuurent iteration: the most similar digit, and the percentage of the similarity
            random = random_change(inputLst[digit])  # Randomize the digit in 10% of the bits
            digitAfterReconstuction = reconstruction_func(random, weightedMatrix)
            diffValue, diffIndex = calculate_diffrence(inputLst, digitAfterReconstuction)  # Check what is the most similar digit, and the percentage of the similarity
            currentData.append(diffIndex)
            currentData.append(diffValue)
            digitLst.append(currentData)
        allData.append(digitLst)
    return allData


def main():
    # Calculate the input matrix
    inputLst = input_to_matrix(num)
    # Calculate the weighted matrix
    weightedMatrix = weighted_matrix_func(inputLst)
    answer = list_of_diffrences(num, inputLst, iter, weightedMatrix)

    # calculate average of number of bits the algorithm succeed to predict
    numOfLine = 0
    for line in answer:
        sum = 0
        counter = 0
        for i in range(len(line)):
            if line[i][0] == numOfLine:
                counter += 1
                sum += (line[i][1])
        if counter != 0:
            print("for " + str(numOfLine) + ": " + str(sum/counter))
        else:
            print("for " + str(numOfLine) + ": 0")
        numOfLine += 1


if __name__ == "__main__":
    # get input from the user
    print("Number of digits to learn: ")
    num = int(input())
    print("Number of iteration: ")
    iter = int(input())
    main()