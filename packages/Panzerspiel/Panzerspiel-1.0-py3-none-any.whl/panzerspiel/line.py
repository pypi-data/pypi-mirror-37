from panzerspiel import vector


class line():
    """
    This class represents a vector line from origin to origin + direction
    It is used to implement a ray rectangle collision.
    Therefor a rectangle is represented as a list of four lines
    """
    def __init__(self, origin, direction):
        """
        The constructor accepts tupels instead of vectors are lines
        are mostly created from rectangles, which stores their values as
        tupels
        """
        self.o = vector.vector(origin[0], origin[1])
        self.v = vector.vector(direction[0], direction[1])


def rect_to_lines(rect):
    """
    This functions returns four lines to represent a rectangle
    """
    global screen
    # From top left to top right
    line1 = line(rect.topleft, (rect.width, 0))
    # From top left to bottom left
    line2 = line(rect.topleft, (0, rect.height))
    # From bottom left to bottom right
    line3 = line(rect.bottomleft, (rect.width, 0))
    # From topright to bottom right
    line4 = line(rect.topright, (0, rect.height))
    # Return all lines as a list
    return [line1, line2, line3, line4]
