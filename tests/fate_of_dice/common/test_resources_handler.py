import unittest

from fate_of_dice.common import ResourcesHandler


class TestResourcesHandler(unittest.TestCase):

    def test_resource_path(self):
        resource_path = ResourcesHandler.get_resources_path()
        self.assertTrue(resource_path.exists())
        self.assertTrue(resource_path.joinpath('config.ini').is_file())

    def test_property(self):
        self.assertTrue(ResourcesHandler.get_property('FATE_OF_DICE_TOKEN', 'default'), 'SET YOUR TOKEN !!!')

    def test_property_default(self):
        self.assertTrue(ResourcesHandler.get_property('NoneExist', 'default'), 'default')


if __name__ == '__main__':
    unittest.main()
