from shape_counter import Point, Shape, Grid, ShapeFinder
import pytest

PIXELS_3X3 = [
    [1, 0, 0], #(0,0) (1,0) (2,0)
    [1, 0, 1], #(0,1) (1,1) (2,1)
    [0, 1, 0], #(0,2) (1,2) (2,2)
]

class TestGrid():

    def test_is_on_true(self):
        grid = Grid(PIXELS_3X3)

        assert grid.is_on(Point(2, 1))

    def test_is_on_false(self):
        grid = Grid(PIXELS_3X3)

        assert grid.is_on(Point(1, 0)) == False

    @pytest.mark.parametrize("point, expected_neighbors", [
        (Point(0, 0), [Point(1, 0), Point(0, 1)]),
        (Point(1, 0), [Point(0, 0), Point(2, 0), Point(1, 1)]),
        (Point(2, 0), [Point(1, 0), Point(2, 1)]),

        (Point(0, 1), [Point(0, 0), Point(1, 1), Point(0, 2)]),
        (Point(1, 1), [Point(1, 0), Point(2, 1), Point(1, 2), Point(0, 1)]),
        (Point(2, 1), [Point(2, 0), Point(1, 1), Point(2, 2)]),

        (Point(0, 2), [Point(0, 1), Point(1, 2)]),
        (Point(1, 2), [Point(0, 2), Point(1, 1), Point(2, 2)]),
        (Point(2, 2), [Point(2, 1), Point(1, 2)])
    ])
    def test_get_neighbors(self, point, expected_neighbors):

        grid = Grid(PIXELS_3X3)
        neighbors = grid.get_neighbors(point)

        #Don't care about order
        assert set(neighbors) == set(expected_neighbors)

class TestShapeFinder():

    def test_find_no_shapes_1x1(self):

        grid = Grid([[0]])

        shapes = self.find_shapes(grid)

        assert len(shapes) == 0

    def test_find_shapes_1x1(self):

        grid = Grid([[1]])

        shapes = self.find_shapes(grid)

        assert shapes == set([make_shape((0, 0))])

    def test_find_shapes_3x3(self):

        grid = Grid(PIXELS_3X3)

        shapes = self.find_shapes(grid)

        assert shapes == set([
            make_shape((0, 0), (0, 1)),
            make_shape((2, 1)),
            make_shape((1, 2))
        ])

    def test_find_s_shape(self):

        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ])

        shapes = self.find_shapes(grid)

        assert shapes == set([make_shape(
            (1, 1), (2, 1), (3, 1),
            (1, 2),
            (1, 3), (2, 3), (3, 3),
            (3, 4),
            (1, 5), (2, 5), (3, 5),
        )])

    def test_find_o_shape(self):

        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ])

        shapes = self.find_shapes(grid)

        assert shapes == set([make_shape(
            (1, 1), (2, 1), (3, 1),
            (1, 2), (3, 2),
            (1, 3), (2, 3), (3, 3),
        )])

    def test_find_shapes_10x4(self):

        grid = Grid([
            [0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
        ])

        shapes = self.find_shapes(grid)

        assert shapes == set([
            make_shape((0, 2)),
            make_shape((1, 1)),
            make_shape((2, 0), (3, 0), (4, 0), (3, 1), (3, 2), (2, 3), (3, 3), (4, 3)),
            make_shape((7, 0), (9, 0), (7, 1), (8, 1), (9, 1), (9, 2), (7, 3), (8, 3), (9, 3))
        ])

    def find_shapes(self, grid):
        shape_finder = ShapeFinder(grid)
        shapes = shape_finder.find_shapes()
        print("Found", shapes)
        return set(shapes)

def make_shape(*point_tuples):

    points = [Point(p[0], p[1]) for p in point_tuples]
    return Shape(frozenset(points))