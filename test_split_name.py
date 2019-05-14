from unittest import TestCase
from SeparateNames import split_name


class TestSplitName(TestCase):  # TODO: still need to add test cases for all class methods.
    test_cases = [
        ['Jorge Sánchez Fernández', 'Jorge', 'Sánchez', 'Fernández', None],
        ['Jorge Sánchez Fernández', 'Jorge', 'Sánchez', 'Fernández', 1],
        ['Jorge Sánchez Fernández', 'Jorge', 'Sánchez', 'Fernández', 0],
        ['Jorge Sánchez Fernández', 'Fernández', 'Jorge', 'Sánchez', -1],
        ['Jorge Sánchez Fernández de la Cueva', 'Jorge', 'Sánchez', 'Fernández de la Cueva', None],
        ['Jorge Sánchez Fernández de la Cueva', 'Jorge', 'Sánchez', 'Fernández de la Cueva', 1],
        ['Jorge Sánchez Fernández de la Cueva', 'Jorge', 'Sánchez', 'Fernández de la Cueva', 0],
        ['Jorge Sánchez Fernández de la Cueva', 'de la Cueva', 'Jorge', 'Sánchez Fernández', -1],
        ['Sánchez Fernández Jorge', 'Jorge', 'Sánchez', 'Fernández', None],
        ['Sánchez Fernández Jorge', 'Sánchez', 'Fernández', 'Jorge', 1],
        ['Sánchez Fernández Jorge', 'Jorge', 'Sánchez', 'Fernández', 0],
        ['Sánchez Fernández Jorge', 'Jorge', 'Sánchez', 'Fernández', -1],
        ['John Smith', 'John', 'Smith', '', None],
        ['John Smith', 'John', 'Smith', '', 1],
        ['John Smith', 'John', 'Smith', '', 0],
        ['John Smith', 'Smith', 'John', '', -1],
        ['Smith John', 'John', 'Smith', '', None],
        ['Smith John', 'Smith', 'John', '', 1],
        ['Smith John', 'John', 'Smith', '', 0],
        ['Smith John', 'John', 'Smith', '', -1],
        ['Louis Van Der Daas', 'Louis', 'Van Der Daas', '', None],
        ['Louis Van Der Daas', 'Louis', 'Van Der Daas', '', 1],
        ['Louis Van Der Daas', 'Louis', 'Van Der Daas', '', 0],
        ['Louis Van Der Daas', 'Van Der Daas', 'Louis', '', -1],
        ['Jorge Sánchez Fernández de la Huerta Herrera', 'Jorge', 'Sánchez Fernández', 'de la Huerta Herrera', None],
        ['Jorge Sánchez Fernández de la Huerta Herrera', 'Jorge', 'Sánchez Fernández', 'de la Huerta Herrera', 1],
        ['Jorge Sánchez Fernández de la Huerta Herrera', 'Jorge', 'Sánchez Fernández', 'de la Huerta Herrera', 0],
        ['Jorge Sánchez Fernández de la Huerta Herrera', 'Herrera', 'Jorge Sánchez', 'Fernández de la Huerta', -1],
        ['Luis Carlos Estrella Lopez', 'Luis Carlos', 'Estrella', 'Lopez', None],
        ['Luis Carlos Estrella Lopez', 'Luis Carlos', 'Estrella', 'Lopez', 1],
        ['Luis Carlos Estrella Lopez', 'Luis Carlos', 'Estrella', 'Lopez', 0]
    ]

    def test_split_name(self):
        for c in self.test_cases:
            if c[4] is None:
                TestCase.assertEqual(self, split_name(c[0]), c[1:4])
            else:
                TestCase.assertEqual(self, split_name(c[0], c[4]), c[1:4])

    def test_split_name_corto(self):
        TestCase.assertEqual(self, split_name('Pepe'), None)
        TestCase.assertEqual(self, split_name(''), None)
