from stdlib.utils.inn import In


class Matrices(object):
    def __init__(self, matrix_one_in: In = None, matrix_two_in: In = None, matrix_one_str: str = None,
                 matrix_two_str: str = None):
        self._m_one = []
        self._m_two = []
        self._m_result = []
        self._one_r = 0
        self._two_r = 0
        self._one_c = 0
        self._two_c = 0
        self._type = 'non'

        if matrix_one_str and matrix_two_str:
            matrix_one_in = In(matrix_one_str)
            matrix_two_in = In(matrix_two_str)

        if matrix_one_in and matrix_two_in:
            try:
                self._one_r = matrix_one_in.read_int()
                self._one_c = matrix_one_in.read_int()
                self._m_one = [[] for i in range(self._one_r)]
                try:
                    for r in range(self._one_r):
                        for c in range(self._one_c):
                            self._m_one[r].append(float(matrix_one_in.read_string()))
                except (IndexError, ValueError) as e:
                    raise e("Invalid input from Matrix Constructor")

                self._two_r = matrix_two_in.read_int()
                self._two_c = matrix_two_in.read_int()
                self._m_two = [[] for i in range(self._two_r)]
                try:
                    for r in range(self._two_r):
                        for c in range(self._two_c):
                            self._m_two[r].append(float(matrix_two_in.read_string()))
                except (IndexError, ValueError) as e:
                    raise e("Invalid input from Matrix Constructor")

            except (IndexError, ValueError) as e:
                raise e("invalid input from Matrix constructor")

    def __validate_matrix_array(self, type):
        """

        :param type:
        :return:
        """
        if type == 'addition':
            if not (self._one_r == self._two_r and self._one_c == self._two_c):
                raise ValueError("For addition your matrices must have the same dimensions")

        if type == 'dot-multiply':
            if not self._one_c == self._two_r:
                raise ValueError("Dot multiplying requires the  # of columns in matrix A to be the same as the # of "
                                 "rows in matrix B")

    def addition(self):
        self.__validate_matrix_array('addition')
        self._m_result = [[] for i in range(self._one_r)]
        for r in range(self._one_r):
            for c in range(self._one_c):
                self._m_result[r].append(self._m_one[r][c] + self._m_two[r][c])

    def dot_multiply(self):
        self.__validate_matrix_array('dot-multiply')
        self._m_result = [[] for i in range(self._one_r)]
        for row in range(self._one_r):
            col = 0
            for r in range(self._one_r):
                col = 0
                for c in range(self._one_c):
                    col += self._m_one[row][c] * self._m_two[c][r]

                    if c + 1 == self._one_c:
                        self._m_result[row].append(col)
                        continue

    def m_one(self):
        return self._m_one

    def m_two(self):
        return self._m_two

    def m_result(self):
        return self._m_result

    def __str__(self):
        matrix = self._m_result
        s = ''
        for row in range(len(matrix)):
            s += '| '
            for col in range(len(matrix[row])):
                s += '{0:7} '.format(int(matrix[row][col]) if matrix[row][col].is_integer() else matrix[row][col])

            s += '|\n'

        return s


def main():
    import os
    dirpath = os.getcwd()
    # inn_one = In('{0}/tests/simple_matrix_one_add.txt'.format(dirpath))
    # inn_two = In('{0}/tests/simple_matrix_two_add.txt'.format(dirpath))
    # matrix = Matrices(inn_one, inn_two)
    # matrix.addition()
    # print(matrix)

    inn_one = In('{0}/tests/matrix_one_dot_mult.txt'.format(dirpath))
    inn_two = In('{0}/tests/matrix_two_dot_mult.txt'.format(dirpath))
    mat = Matrices(inn_two, inn_one)
    mat.dot_multiply()
    print(mat)


if __name__ == '__main__':
    main()
