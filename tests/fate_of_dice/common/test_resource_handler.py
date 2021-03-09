import unittest

from pathlib import Path

from fate_of_dice.common.resource_handler import ResourceHandler


class TestResourcesHandler(unittest.TestCase):

    def test_default_resource_path(self):
        result = ResourceHandler.get_resources_path()
        self.assertTrue(result.exists())
        self.assertRegex(str(result), str(Path('resources/')))

    def test_resource_path(self):
        resource_path = ResourceHandler.get_resources_path()
        self.assertTrue(resource_path.exists())
        self.assertTrue(resource_path.joinpath('config.ini').is_file())

    def test_property(self):
        self.assertTrue(ResourceHandler.get_property('FATE_OF_DICE_TOKEN', 'default'), 'SET YOUR TOKEN !!!')

    def test_property_default(self):
        self.assertTrue(ResourceHandler.get_property('NoneExist', 'default'), 'default')


if __name__ == '__main__':
    unittest.main()
