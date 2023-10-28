import pytest

from tools.errors import PointError
from tools.point import Point, Point2D, Point3D


class TestPoint:
    def test_init(self):
        p = Point(1, 2, 3)
        assert p == Point(1, 2, 3)

    def test_steps(self):
        p = Point()
        assert p.steps == {}

    def test_x(self):
        p = Point(1, 2, 3)
        assert p == (1, 2, 3)

    def test_tup(self):
        p = Point(1, 2, 3)
        assert p.tup() == (1, 2, 3)

    def test_repr(self):
        p = Point(1, 2, 3)
        assert repr(p) == "(1,2,3)"

    def test_eq(self):
        p1 = Point(1, 2, 3)
        p2 = Point(1, 2, 3)
        assert p1 == p2

    def test_add(self):
        p1 = Point(1, 2, 3)
        p2 = Point(4, 5, 6)
        result = p1 + p2
        assert result == Point(5, 7, 9)

    def test_sub(self):
        p1 = Point(4, 5, 6)
        p2 = Point(1, 2, 3)
        result = p1 - p2
        assert result == Point(3, 3, 3)

    def test_copy(self):
        p1 = Point(1, 2, 3)
        p2 = p1.copy()
        assert p1 is not p2
        assert p1 == p2

    def test_abs(self):
        p = Point(-1, -2, -3)
        assert abs(p) == 6

    def test_iadd(self):
        p1 = Point(1, 2, 3)
        p2 = Point(4, 5, 6)
        p1 += p2
        assert p1 == Point(5, 7, 9)

    def test_isub(self):
        p1 = Point(4, 5, 6)
        p2 = Point(1, 2, 3)
        p1 -= p2
        assert p1 == Point(3, 3, 3)

    def test_hash(self):
        p = Point(1, 2, 3)
        assert hash(p) == hash((1, 2, 3))

    def test_len(self):
        p = Point(1, 2, 3)
        assert len(p) == 3

    def test_integer_division(self):
        p = Point(4, 6)
        result = p // 2
        assert result == Point(2, 3)

        p = Point(4, 6, 8)
        result = p // 2
        assert result == Point(2, 3, 4)

        p = Point(9, 3)
        result = p // 2
        assert result == Point(4, 1)

        p = Point(10, 20)
        result = p // 3
        assert result == Point(3, 6)


class TestPoint2D:
    def test_init(self):
        p = Point2D(1, 2)
        assert p.x == 1
        assert p.y == 2

    def test_distance_to_manhatten(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(4, 6)
        distance = p1.distance_to(p2)
        assert distance == 7

    def test_distance_to_hypotentuse(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(4, 6)
        distance = p1.distance_to(p2, order=2)
        assert distance == pytest.approx(5)

    def test_add(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(3, 4)
        result = p1 + p2
        assert result.x == 4
        assert result.y == 6

    def test_sub(self):
        p1 = Point2D(4, 6)
        p2 = Point2D(1, 2)
        result = p1 - p2
        assert result.x == 3
        assert result.y == 4

    def test_mul(self):
        p = Point2D(2, 3)
        result = p * 2
        assert result.x == 4
        assert result.y == 6

    def test_truediv(self):
        p = Point2D(4, 6)
        result = p / 2
        assert result.x == 2.0
        assert result.y == 3.0

    def test_iadd(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(3, 4)
        p1 += p2
        assert p1.x == 4
        assert p1.y == 6

    def test_isub(self):
        p1 = Point2D(4, 6)
        p2 = Point2D(1, 2)
        p1 -= p2
        assert p1.x == 3
        assert p1.y == 4

    def test_imul(self):
        p = Point2D(2, 3)
        p *= 2
        assert p.x == 4
        assert p.y == 6

    def test_itruediv(self):
        p = Point2D(4, 6)
        p /= 2
        assert p.x == 2.0
        assert p.y == 3.0

    def test_eq(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(1, 2)
        assert p1 == p2

    def test_ne(self):
        p1 = Point2D(1, 2)
        p2 = Point2D(3, 4)
        assert p1 != p2

    def test_zero_values(self):
        p = Point2D(0, 0)
        assert p.x == 0
        assert p.y == 0

        p += Point2D(0, 0)
        assert p.x == 0
        assert p.y == 0

        p -= Point2D(0, 0)
        assert p.x == 0
        assert p.y == 0

        p *= 0
        assert p.x == 0
        assert p.y == 0

        with pytest.raises(ZeroDivisionError):
            p /= 0

    def test_negative_values(self):
        p = Point2D(-1, -2)
        assert p.x == -1
        assert p.y == -2

        result = p + Point2D(-3, -4)
        assert result.x == -4
        assert result.y == -6

    def test_nb4(self):
        p = Point2D(1, 2)
        neighbors = list(p.nb4())

        assert len(neighbors) == 4
        assert Point2D(1, 1) in neighbors
        assert Point2D(1, 3) in neighbors
        assert Point2D(0, 2) in neighbors
        assert Point2D(2, 2) in neighbors

    def test_nb4_with_finite_grid(self):
        p = Point2D(1, 1)
        neighbors = list(p.nb4(grid_size=2))

        assert len(neighbors) == 2
        assert Point2D(0, 1) in neighbors
        assert Point2D(1, 0) in neighbors

    def test_all_neighours_bad_starting_point(self):
        p = Point2D(2, 1)
        neighbors = p.all_neighbours(grid_size=2)

        with pytest.raises(PointError):
            next(neighbors)

    def test_all_neighours_nb4(self):
        p = Point2D(0, 0)
        neighbors = list(p.nb4())

        assert len(neighbors) == 4
        assert Point(1, 0) in neighbors
        assert Point(0, 1) in neighbors
        assert Point(-1, 0) in neighbors
        assert Point(0, -1) in neighbors

    def test_all_neighours_nb8(self):
        p = Point2D(0, 0)
        neighbors = list(p.nb8())

        assert len(neighbors) == 8

        assert Point(1, 0) in neighbors
        assert Point(0, 1) in neighbors
        assert Point(-1, 0) in neighbors
        assert Point(0, -1) in neighbors

        assert Point(1, 1) in neighbors
        assert Point(-1, -1) in neighbors
        assert Point(-1, 1) in neighbors
        assert Point(1, -1) in neighbors

    def test_all_neighours_nb4_grid_size_int(self):
        p = Point2D(0, 0)
        neighbors = list(p.nb4(grid_size=2))

        assert len(neighbors) == 2
        assert Point(1, 0) in neighbors
        assert Point(0, 1) in neighbors

    def test_all_neighours_nb8_grid_size_int(self):
        p = Point2D(0, 0)
        neighbors = list(p.nb8(grid_size=2))

        assert len(neighbors) == 3

        assert Point(1, 0) in neighbors
        assert Point(0, 1) in neighbors

        assert Point(1, 1) in neighbors

    def test_all_neighours_nb4_grid_size_tuple(self):
        p = Point2D(0, 0)
        neighbors = list(p.nb4(grid_size=(1, 2)))

        assert len(neighbors) == 1
        assert Point(0, 1) in neighbors

    def test_all_neighours_nb8_grid_size_tuple(self):
        p = Point2D(0, 0)
        neighbors = list(p.nb8(grid_size=(2, 3)))

        assert len(neighbors) == 3

        assert Point(1, 0) in neighbors
        assert Point(0, 1) in neighbors

        assert Point(1, 1) in neighbors


class TestPoint3D:
    def test_init(self):
        p = Point3D(1, 2, 3)
        assert p.x == 1
        assert p.y == 2
        assert p.z == 3

    def test_distance_to_manhattan(self):
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(4, 6, 8)
        distance = p1.distance_to(p2)
        assert distance == 12

    def test_distance_to_euclidean(self):
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(4, 6, 8)
        distance = p1.distance_to(p2, order=2)
        assert distance == pytest.approx(7.0710678118654755)

    def test_nb6(self):
        p = Point3D(1, 2, 3)
        neighbors = list(p.nb6())

        assert len(neighbors) == 6
        assert Point3D(0, 2, 3) in neighbors
        assert Point3D(2, 2, 3) in neighbors
        assert Point3D(1, 1, 3) in neighbors
        assert Point3D(1, 3, 3) in neighbors
        assert Point3D(1, 2, 2) in neighbors
        assert Point3D(1, 2, 4) in neighbors

    def test_all_neighours(self):
        p = Point3D(0, 0, 0)
        neighbors = list(p.all_neighbours())

        assert len(neighbors) == 26
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    if (x, y, z) == (0, 0, 0):
                        continue
                    print(x, y, z)
                    assert Point3D(x, y, z) in neighbors
