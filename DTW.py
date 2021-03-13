import math
import sys

# example cat data
def parseFile(input_file):
    with open(input_file) as textFile:
        w, h = [int(x) for x in next(textFile).split()] # read first line
        input = [ ]
        for line in textFile: # read rest of lines
            input.append([int(x) for x in line.split()])         
    return input

def d1(a, b): # distance function for cat data 
    we_diff = abs(a[0] - b[0])
    wh_diff = abs(a[1] - b[1])
    me_diff = abs(a[2] - b[2])

    return we_diff * 1.5 + wh_diff * 3.0 + me_diff * .5

def d2(c, d): # distance function for euclidean points
    sum = 0
    for i in range(len(c)):
        sum += (c[i] - d[i]) ** 2
    return math.sqrt(sum)

def dtw(A, B, d):
    # initialization
    n, m = len(A), len(B)
    dtw = [[math.inf for j in range(m+1)] for i in range(n+1)]
    ptr = [[(-1, -1) for j in range(m+1)] for i in range(n+1)]
    dtw[0][0] = 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = d(A[i-1], B[j-1]) # cost of matching A[i-1] to B[j-1]
            a, b, c = dtw[i-1][j], dtw[i][j-1], dtw[i-1][j-1] # minimum cost out of three prior matching choices
            dtw[i][j] = cost + min(a, b, c) # final cost for entry

            # lookback pointer calculation
            if a < b and a < c: 
                ptr[i][j] = (i-1, j)
            elif b < a and b < c:
                ptr[i][j] = (i, j-1)
            else:
                ptr[i][j] = (i-1, j-1)

    # path initialization
    path = [(n-1, m-1)]
    cell = ptr[n][m]

    while cell[0] + cell[1] != 0: # path backtracing
        i, j = cell[0], cell[1]
        path.insert(0, (i - 1, j - 1)) # correct for 1 offset in dtw array
        cell = ptr[i][j]

    return dtw[n][m], path

if __name__=="__main__":
    print("Default example: Cat data with weight, whiskers, meows/hr")

    if len(sys.argv) == 4:
        #parsing the data from the text files
        input1 = parseFile(sys.argv[1])
        input2 = parseFile(sys.argv[2])

        #checking the command line arguments and run the appropriate distance function
        if str(sys.argv[3]) == "-c":
            dst, path = dtw(input1, input2, d1)
        elif str(sys.argv[3]) == "-e":
            dst, path = dtw(input1, input2, d2)
        else:
            print("Bad format for distance function.")
            print("Use -c for cat distance, -e for euclidean")

        #print results
        print("Cost: " + str(dst))
        print("Path: " + str(path))
    else:
        print("Usage: DTW.py <input_file_A> <input_file_B> <-c|-o>")


