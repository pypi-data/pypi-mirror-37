import math
import random
from typing import List, Union, Any

from stdlib.stdlib.complex import Complex


class FFT:
    def __init__(self):
        self.__ZERO = Complex(0, 0)

    @property
    def __ZERO(self):
        return self.__ZERO

    @__ZERO.setter
    def __ZERO(self, value):
        self.___ZERO = value

    def fft(self, x: List[Complex]) -> Union[list, List[Union[range, Any]]]:
        """
        Returns the FFT of the specified complex array.
        :param x: the Complex array
        :return: the FFT of the complex array {@param x}
        """
        n = len(x)
        if n == 1:
            return [x[0]]

        if n % 2 != 0:
            raise ValueError("n is not a power of 2. n = {}".format(n))

        even = list(range(int(n / 2)))

        for k in range(int(n / 2)):
            even[k] = x[2 * k]

        q = self.fft(even)
        odd = even

        for k in range(int(n / 2)):
            odd[k] = x[2 * k + 1]

        r = self.fft(odd)  # also supposed to be a complex array
        y = list(range(n))

        for k in range(int(n / 2)):
            kth = float(-2 * k * math.pi / n)
            wk = Complex(math.cos(kth), math.sin(kth))
            y[k] = q[k].plus(wk.times(r[k]))
            y[int(k + n / 2)] = q[k].minus(wk.times(r[k]))

        return y

    def ifft(self, x: List[Complex]) -> Union[list, List[Union[range, Any]]]:
        """
        Returns the inverse FFT of the specified complex array.
        :param x: the Complex array
        :return: the inverse FFT of the specified complex array.
        """
        n = len(x)
        y = list(range(n))
        for i in range(n):
            y[i] = type(Complex)(x[i].conjugate())

        y = self.fft(y)

        for i in range(n):
            y[i] = y[i].conjugate()

        for i in range(n):
            y[i] = y[i].scale(1.0 / n)

        return y

    def cir_convolve(self, x: List[Complex], y: List[Complex]) -> Union[list, List[Union[range, Any]]]:
        """
        Returns the circular convolution of the two specified complex arrays
        :param x: one Complex array
        :param y: the other Complex array
        :return: the circular convolution of the two specified complex arrays
        """
        if len(x) != len(y):
            raise ValueError("Dimensions don't agree")

        n = len(x)
        a = self.fft(x)
        b = self.fft(y)

        c = list(range(n))
        for i in range(n):
            c[i] = a[i].times(b[i])

        return self.ifft(c)

    def lin_convolve(self, x: List[Complex], y: List[Complex]) -> Union[List[Complex], List[Complex]]:
        """
        Returns the linear convolution of the two specified complex arrays.
        :param x: one Complex array
        :param y: the other Complex array
        :return: the linear convolution of the two specified complex arrays
        """
        a = list(range(int(2 * len(x))))
        for i in range(len(x)):
            a[i] = x[i]

        for i in range(len(x), int(2 * len(x))):
            a[i] = self.__ZERO

        b = list(range(int(2 * len(y))))
        for i in range(len(y)):
            b[i] = y[i]

        for i in range(len(y), int(2 * len(y))):
            b[i] = self.__ZERO

        return self.cir_convolve(a, b)

    @staticmethod
    def _show(x: List[Complex], title: str):
        print(title)
        print('-----------------')
        for i in range(len(x)):
            print(x[i])

        print('\n')

    def main(self, size: int):
        x = list(range(size))

        for i in range(size):
            x[i] = Complex(i, 0)
            x[i] = Complex(random.randint(-1, 1), 0)

        self._show(x, 'x')

        y = self.fft(x)
        self._show(y, 'y = fft(x)')

        z = self.ifft(x=y)
        self._show(z, 'z = ifft(y)')

        c = self.cir_convolve(x, x)
        self._show(c, 'c = circular convolve(x, x)')

        d = self.lin_convolve(x, x)
        self._show(d, 'd = linear convolve(x, x)')


if __name__ == '__main__':
    fft = FFT()
    fft.main(size=100)
