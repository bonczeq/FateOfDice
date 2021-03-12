import unittest

from fate_of_dice.resources.resource_handler import ResourceImageHandler


class TestResourceImageHandler(unittest.TestCase):
    def test_resource_path(self):
        result = ResourceImageHandler.get_resources_path()
        self.assertTrue(result.exists())
        self.assertRegex(result.name, 'icons')

    def test_variables_exist(self):
        self.assertTrue(ResourceImageHandler.FATE_OF_DICE_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.CRITICAL_FAILURE_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.FAILURE_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.SUCCESS_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.EXTREMAL_SUCCESS_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.CRITICAL_SUCCESS_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.INNOVATION_IMAGE_PATH.exists())
        self.assertTrue(ResourceImageHandler.PROCESS_IMAGE_PATH.exists())


if __name__ == '__main__':
    unittest.main()
