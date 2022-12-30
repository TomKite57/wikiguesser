#==============================================================================#
# Imports
import os

# levenshtein algorithm
def string_distance(str1, str2):
    mat = [[0 for _ in range(len(str1)+1)] for _ in range(len(str2)+1)]
    mat[0] = [i for i in range(len(str1)+1)]
    for i in range(len(str2)+1):
        mat[i][0] = i

    for i, s2 in enumerate(str2):
        for j, s1 in enumerate(str1):
            if s1==s2:
                mat[i+1][j+1] = mat[i][j]
            else:
                mat[i+1][j+1] = min(mat[i][j], mat[i+1][j], mat[i][j+1]) + 1

    return mat[-1][-1]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
