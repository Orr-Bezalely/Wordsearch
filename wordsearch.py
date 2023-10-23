# IMPORTS
import sys, os, time
##############################################
# GLOBAL VARIABLES - MESSAGES AND OTHER VARIABLES
ARGS_LENGTH = 4
WRONG_ARG_NUMBER = "There is an incorrect amount of arguments"
WORD_FILE_NOT_FOUND = "The word file does not exist"
MATRIX_FILE_NOT_FOUND = "The matrix file does not exist"
INVALID_DIRECTION_STRING = "The direction string_made is invalid"
COMMA = ","
UP = "u"
DOWN = "d"
LEFT = "l"
RIGHT = "r"
UP_RIGHT = "w"
UP_LEFT = "x"
DOWN_RIGHT = "y"
DOWN_LEFT = "z"
POSSIBLE_DIRECTION_STRING = "udlrwxyz"


##############################################
# FUNCTIONS
def file_not_exists_check(filename):
    """
    Takes in a filename and returns False if the file exists and True if the
     file doesn't exist
    :param filename: string_made which contains file name
    :return: boolean of whether the file exists
    """
    return not(os.path.isfile(filename))


def check_direction_invalidity(directions):
    """
    Takes in the directions string_made and returns False if they are valid
    and True if they are invalid
    :param directions: string_made of possible directions
    :return: boolean of whether the directions string_made is valid or not
    """
    return not all(i in POSSIBLE_DIRECTION_STRING for i in directions)


def check_input_args(args):
    """
    Takes in a list containing the arguments sent to the program and returns
    string_made explaining what the error is (and returns None if no errors)
    :param args: list containing arguments sent to program
    :return: None if no errors, string_made explaining error if there is some
    """
    if len(args) != ARGS_LENGTH: return WRONG_ARG_NUMBER
    elif file_not_exists_check(args[0]): return WORD_FILE_NOT_FOUND
    elif file_not_exists_check(args[1]): return MATRIX_FILE_NOT_FOUND
    elif check_direction_invalidity(args[3]): return INVALID_DIRECTION_STRING
    else: return None


def read_wordlist_file(filename):
    """
    Takes in the file name which contains the possible words and returns them
    as a list
    :param filename: string_made containing file name of words
    :return: list containing all of the defined words
    """
    with open(filename, "r") as word_file:
        words = [line.strip() for line in word_file]
    return words


def read_matrix_file(filename):
    """
    Takes in the file name which contains the matrix and returns the matrix
    as a 2-dimensional list
    :param filename: string_made containing file name of matrix
    :return: 2-dimensional list of letters
    """
    with open(filename, "r") as matrix_file:
        lines = [line.strip().split(",") for line in matrix_file]
    return lines


def vertically(coords, matrix, sign, word):
    """
    Takes in the coordinates where the first letter appears, matrix,
    sign and word and returns the amount of times the word appeared in the
    vertical plane of search
    :param coords: list of tuples each containing the row and column index
    :param matrix: 2-dimensional list of letters
    :param sign: number representing direction to check word
    :param word: string_made which contains the word to check for
    :return: number of times word appeared in vertical plane of search
    """
    counter = 0
    for start in coords:
        end = start[0] + (len(word)-1)*sign
        row_check = bool(0 <= end <= len(matrix)-1)
        if not row_check: continue
        column = [matrix[i][start[1]] for i in range(start[0], end+sign, sign)]
        if "".join(column) == word: counter += 1
    return counter


def horizontally(coords, matrix, sign, word):
    """
    Takes in the coordinates where the first letter appears, matrix,
    sign and word and returns the amount of times the word appeared in the
    horizontal plane of search
    :param coords: list of tuples each containing the row and column index
    :param matrix: 2-dimensional list of letters
    :param sign: number representing direction to check word
    :param word: string_made which contains the word to check for
    :return: number of times word appeared in horizontal plane of search
    """
    counter = 0
    for start in coords:
        end = start[1] + (len(word)-1)*sign
        column_check = bool(0 <= end <= len(matrix[0])-1)
        if not column_check: continue
        row = [matrix[start[0]][i] for i in range(start[1], end+sign, sign)]
        if "".join(row) == word: counter += 1
    return counter


def diag_x_y(coords, matrix, sign, word):
    """
    Takes in the coordinates where the first letter appears, matrix,
    sign and word and returns the amount of times the word appeared in the
    y=-x+c plane of search
    :param coords: list of tuples each containing the row and column index
    :param matrix: 2-dimensional list of letters
    :param sign: number representing direction to check word
    :param word: string_made which contains the word to check for
    :return: number of times word appeared in y=-x+c plane of search
    """
    counter = 0
    for start in coords:
        end_row = start[0] + (len(word)-1)*sign
        end_inner = start[1] + (len(word)-1)*sign
        row_check = bool(0 <= end_inner <= len(matrix[0])-1)
        column_check = bool(0 <= end_row <= len(matrix)-1)
        if not(row_check and column_check): continue
        diag = [matrix[start[0]+i][start[1]+i]
                for i in range(0, sign*len(word), sign)]
        if "".join(diag) == word: counter += 1
    return counter


def diag_w_z(coords, matrix, sign, word):
    """
    Takes in the coordinates where the first letter appears, matrix,
    sign and word and returns the amount of times the word appeared in the
    y=x+c plane of search
    :param coords: list of tuples each containing the row and column index
    :param matrix: 2-dimensional list of letters
    :param sign: number representing direction to check word
    :param word: string_made which contains the word to check for
    :return: number of times word appeared in y=x+c plane of search
    """
    counter = 0
    for start in coords:
        end_row = start[0] - (len(word)-1)*sign
        end_inner = start[1] + (len(word)-1)*sign
        row_check = bool(0 <= end_inner <= len(matrix[0])-1)
        column_check = bool(0 <= end_row <= len(matrix)-1)
        if not(row_check and column_check): continue
        diag = [matrix[start[0]-i][start[1]+i]
                for i in range(0, sign*len(word), sign)]
        if "".join(diag) == word: counter += 1
    return counter


def find_coords(word_list, matrix):
    """
    Takes in the word list and the matrix and returns the coordinates of the
    places the first letter in each of the words is found
    :param word_list: list containing all of the defined words
    :param matrix: 2-dimensional list of letters
    :return: dictionary containing the coordinates of the places the first
    letter in each of the words is found
    """
    coord_dict = {}
    for word in word_list:
        letter = word[0]
        if letter not in coord_dict:
            coord_dict[letter] = [(i, j) for i in range(len(matrix)) for
                                  j in range(len(matrix[i])) if
                                  matrix[i][j] == letter]
    return coord_dict


def find_words_in_matrix(word_list, matrix, ways):
    """
    Takes in the word list, 2-dimentional list of letters and the string_made
    representing the directions to search and returns a list of tuples which
    contains the number of times the word is found
    :param word_list: list containing all of the defined words
    :param matrix: 2-dimensional list of letters
    :param ways: string_made representing directions to search
    :return: list of tuples which contains the number of times the word is
    found
    """
    results = []
    first_letter_coords_dict = find_coords(word_list, matrix)
    for word in word_list:
        count, coords_list = 0, first_letter_coords_dict[word[0]]
        if UP in ways: count += vertically(coords_list, matrix, -1, word)
        if DOWN in ways: count += vertically(coords_list, matrix, 1, word)
        if LEFT in ways: count += horizontally(coords_list, matrix, -1, word)
        if RIGHT in ways: count += horizontally(coords_list, matrix, 1, word)
        if UP_RIGHT in ways: count += diag_w_z(coords_list, matrix, 1, word)
        if UP_LEFT in ways: count += diag_x_y(coords_list, matrix, -1, word)
        if DOWN_RIGHT in ways: count += diag_x_y(coords_list, matrix, 1, word)
        if DOWN_LEFT in ways: count += diag_w_z(coords_list, matrix, -1, word)
        if count > 0: results.append((word, count))
    return results


def write_output_file(results, output_filename):
    """
    Takes a list of tuples and a file name and outputs them into the file
    :param results: list of tuples containing word and number of times it
    appeared
    :param output_filename: string_made which contains file name
    :return: None
    """
    with open(output_filename, "w") as output_file:
        output_file.writelines(results[i][0] + COMMA + str(results[i][1]) +
                               "\n" for i in range(len(results)))


def main():
    """
    Combines all of the functions together and combines the program
    :return: None
    """
    args = sys.argv[1:]
    check_args_return = check_input_args(args)
    if check_args_return is None:
        words_list = read_wordlist_file(args[0])
        #words_list.sort(key=str.lower)
        matrix_list = read_matrix_file(args[1])
        results = find_words_in_matrix(words_list, matrix_list, args[3])
        #print(results)
        write_output_file(results, args[2])
    else:
        print(check_args_return)

#############################################################


# MAIN PROGRAM
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end-start)

