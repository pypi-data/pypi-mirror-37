import math


class RectHV(object):
    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        if math.isnan(xmin) or math.isnan(xmax):
            raise ValueError("x-coordinate is NaN: " + self.__str__())

        if math.isnan(ymin) or math.isnan(ymax):
            raise ValueError('y-coordinate is Nan: ' + self.__str__())

        if xmax < xmin:
            raise ValueError("xmax < xmin: " + self.__str__())

        if ymax < ymin:
            raise ValueError("ymax < ymin: " + self.__str__())

    def width(self) -> float:
        return self.xmax - self.xmin

    def height(self) -> float:
        return self.ymax - self.ymin

    def intersects(self, that):
        return self.xmax >= that.xmin and self.ymax >= that.ymin and \
               that.xmax >= self.xmin and that.ymax >= self.ymin

    def __contains__(self, item):
        pass

    def __str__(self):
        return ''