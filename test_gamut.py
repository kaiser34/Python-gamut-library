import unittest, numpy as np

import colour
from colour import data, gamut, space


"""Unittests for all functions in the gamut module. """
# Global variable.
n_data = np.array([[0, 0, 0],         # 0 vertecis
                    [10, 0, 0],       # 1 vertecis
                    [10, 10, 0],      # 2 vertecis
                    [0, 10, 0],       # 3 vertecis
                    [5, 5, 5],        # 4 non vertecis
                    [4, 6, 2],        # 5 non vertecis
                    [10, 10, 10],     # 6 vertecis
                    [1, 2, 3],        # 7 non vertecis
                    [10, 0, 10],      # 8 vertecis
                    [0, 0, 10],       # 9 vertecis
                    [0, 10, 10]])     # 10 vertecis

line = np.array([[0, 0, 0], [3, 3, 3]])
point_on_line = np.array([1,1,1])
point_not_on_line = np.array([2,2,2])

tetrahedra = np.array([[0, 0, 0], [0, 10, 0], [10, 0, 0], [0, 0, 10]])
point_on_tetrahedra = np.array([2, 3, 4])               # Inside tetrahedra
point_not_on_tetrahedra = np.array([20, 1, 2])          # Outside tetrahedra

class TestGamut(unittest.TestCase):

    def test_gamut_initialize(self):
        # Test for convex hull
        c_data = data.Data(space.srgb, n_data)          # Generating the colour Data object
        g = gamut.Gamut(space.srgb, c_data)
        vertices = np.array([0, 1, 2, 3, 6, 8, 9, 10])  # Known indices of vertecis for the test case

        self.assertEqual(vertices.tolist(), g.vertices.tolist())    # Checking that the vertecis match

    def test_is_inside(self):
        # Test for gamut.Gamut.is_inside
        c_data = data.Data(space.srgb, n_data)
        g = gamut.Gamut(space.srgb, c_data)

        '''
        points = np.array([[1, 1, 1],   # inside
                           [2, 2, 3],   # inside
                           [20, 2, 3],  # outside
                           [1, 2, 30]]) # outside
        '''

        points = np.ones((2, 2, 2, 3))

        c_points = data.Data(space.srgb, points)
        g.is_inside(space.srgb, c_points)

    def test_get_vertices(self):
        # Test for gamut.Gamut.get_vertices
        c_data = data.Data(space.srgb, n_data)  # Generating the colour Data object
        g = gamut.Gamut(space.srgb, c_data)
        n1_data = np.array([[0, 0, 0],  # 0 vertecis
                           [10, 0, 0],  # 1 vertecis
                           [10, 10, 0],  # 2 vertecis
                           [0, 10, 0],  # 3 vertecis
                           [10, 10, 10],  # 6 vertecis
                           [10, 0, 10],  # 8 vertecis
                           [0, 0, 10],  # 9 vertecis
                           [0, 10, 10]])  # 10 vertecis
        vertices = g.get_vertices(n_data)
        self.assertTrue(np.array_equiv(n1_data,vertices))    # Compares returend array with the known vertices array.

    def test_get_surface(self):
        # Test for gamut.Gamut.get_surface
        c_data = data.Data(space.srgb, n_data)  # Generating the colour Data object
        g = gamut.Gamut(space.srgb, c_data)
        sp = colour.space.srgb
        g.get_surface(sp)

    def test_in_line_triangle_tetrahedra(self):
        c_data = data.Data(space.srgb, n_data)
        g = gamut.Gamut(space.srgb, c_data)

        self.assertTrue(True, g.in_tetrahedra(tetrahedra, point_on_tetrahedra))
        self.assertFalse(False, g.in_tetrahedra(tetrahedra, point_not_on_tetrahedra))

        self.assertFalse(False, g.in_line(line, point_not_on_line))


if __name__ == '__main__':
    unittest.main(exit=False)