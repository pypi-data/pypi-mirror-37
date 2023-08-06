import math


class Complex:
    def __init__(self, real: float, imag: float):
        self.__real = real
        self.__imag = imag

    def __str__(self):
        if self.__imag == 0:
            return str(self.__real) + ''
        if self.__real == 0:
            return str(self.__imag) + 'i'
        if self.__imag < 0:
            return '{} - {}i'.format(self.__real, -self.__imag)
        return '{} + {}i'.format(self.__real, self.__imag)

    def abs(self):
        """
        Returns the absolute value of this complex number.
        :return: the absolute value of this complex number.
        """
        return math.hypot(self.__real, self.__imag)

    def phase(self):
        """
        Returns the phase of this complex number.
        :return: the phase of this complex number.
        """
        return math.atan2(self.__imag, self.__real)

    def plus(self, that):
        """
        Returns the sum of this complex number and the specified complex number.
        :param that: the other Complex number
        :return: the complex number whose value is this + that
        """
        real = float(self.__real + that.__real)
        imag = float(self.__imag + that.__imag)
        return Complex(real, imag)

    def minux(self, that):
        """
        Returns the result of subtracting the specified complex number from this complex number.
        :param that: the other Complex number
        :return: the result of subtracting the specified complex number from this complex number.
        """
        real = float(self.__real - that.__real)
        imag = float(self.__imag - that.__imag)
        return Complex(real, imag)

    def times(self, that):
        """
        Returns the product of this complex number and the specified complex number.
        :param that: the other Complex number
        :return: the product of this complex number and the specified complex number.
        """
        real = float((self.__real * that.__real) - (self.__imag * that.__imag))
        imag = float((self.__real * that.__imag) + (self.__imag * that.__real))
        return Complex(real, imag)

    def scale(self, alpha: float):
        """
        Returns the product of this complex number and the specified scalar.
        :param alpha: the scalar
        :return: the product of this complex number and the specified scalar.
        """
        return Complex(alpha * self.__real, alpha * self.__imag)

    def conjugate(self):
        """
        Returns the complex conjugate of this complex number.
        :return: the complex conjugate of this complex number.
        """
        return Complex(self.__real, -self.__imag)

    def reciprocal(self):
        """
        Returns the reciprocal of the Complex number
        :return: the complex number whose value is 1 / this
        """
        scale = float((self.__real * self.__real) + (self.__imag * self.__imag))
        return Complex(self.__real / scale, -self.__imag / scale)

    def divides(self, that):
        """
        Returns the result of dividing the specified complex number into this complex number.
        :param that: the other complex number
        :return: the complex number whose value is self / that
        """
        return self.times(that.reciprocal())

    def exp(self):
        """
        Returns the complex exponential of this complex number.
        :return: the complex exponential of this complex number.
        """
        return Complex(math.exp(self.__real) * math.cos(self.__imag), math.exp(self.__real) * math.sin(self.__imag))

    def sin(self):
        """
        Returns the complex sine of this complex number.
        :return: the complex sine of this complex number.
        """
        return Complex(math.sin(self.__real) * math.cosh(self.__imag), math.cos(self.__real) * math.sinh(self.__imag))

    def cos(self):
        """
        Returns the complex cosine of this complex number.
        :return: the complex cosine of this complex number.
        """
        return Complex(math.cos(self.__real) * math.cosh(self.__imag), -math.sin(self.__real) * math.sinh(self.__imag))

    def tan(self):
        """
        Returns the complex tangent of this complex number.
        :return: the complex tangent of this complex number.
        """
        return self.sin().divides(self.cos())


