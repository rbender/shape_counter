from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

Shape = namedtuple("Shape", ["points"])

class Grid:

    def __init__(self, pixels):

        self.pixels = pixels

        # For calculating neighbors
        self.max_x = len(pixels[0]) - 1
        self.max_y = len(pixels) - 1

        self.points = self.build_points()

    def build_points(self):
        return [Point(x,y) for y in range(self.max_y + 1) for x in range(self.max_x + 1)]

    def is_on(self, point):
        return self.pixels[point.y][point.x] == 1

    def get_neighbors(self, point):

        x = point.x
        y = point.y

        neighbors = []

        # North
        if y > 0:
            neighbors.append(Point(x, y - 1))

        # South
        if y < self.max_y:
            neighbors.append(Point(x, y + 1))

        # West
        if x > 0:
            neighbors.append(Point(x - 1, y))

        # East
        if x < self.max_x:
            neighbors.append(Point(x + 1, y))

        return neighbors

class ShapeFinder:

    def __init__(self, grid):

        self.grid = grid
        self.visited_points = set()

    def find_shapes(self):

        shapes = []

        for point in self.grid.points:

            if point not in self.visited_points:
                print("Visit", point)

                if self.grid.is_on(point):
                    shape = self.find_shape(point)
                    shapes.append(shape)

                else:
                    self.visited_points.add(point)

            else:
                print("Already visited", point)

        return shapes

    def find_shape(self, point):

        print("Find shape starting at", point)

        # Start a depth first search to find all points in the shape
        shape_points = self.explore_shape(point)

        # Use frozenset so equality checks in unit tests work
        return Shape(frozenset(shape_points))

    def explore_shape(self, point):

        shape_points = set([point])
        self.visited_points.add(point)

        neighbors = self.grid.get_neighbors(point)
        for neighbor in neighbors:

            if neighbor not in self.visited_points:

                if self.grid.is_on(neighbor):
                    shape_points.update(self.explore_shape(neighbor))
                else:
                    self.visited_points.add(neighbor)

        return shape_points

if __name__ == "__main__":

    pixels = [
        [1, 0, 0],
        [0, 1, 1],
        [0, 0, 1],
        [1, 0, 0]
    ]

    grid = Grid(pixels)
    shape_finder = ShapeFinder(grid)

    shapes = shape_finder.find_shapes()

    print("Found {} shapes".format(len(shapes)))
    print("Shapes:", shapes)