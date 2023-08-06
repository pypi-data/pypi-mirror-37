import unittest
import os

from thriftgen.model.file_loader import load_model_from_file
from thriftgen.model.ThriftyEnum import ThriftyEnum
from thriftgen.model.ThriftyStruct import ThriftyStruct
from thriftgen.model.ThriftyException import ThriftyException
from thriftgen.model.ThriftyService import ThriftyService


class TestFileLoader(unittest.TestCase):
    """
    Test creating models from thrift files.
    """
    def test_file_loading(self):
        """
        Test the basic echo thrift file loading.
        """
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/echo.thrift')

        model = load_model_from_file(file_name)
        self.assertEqual(4, len(model.file_items),
                         "There should be an exception, a struct, an enum and a service")

        # ====================================================
        # Enum reading
        # ====================================================
        first_item: ThriftyEnum = model.file_items[0]
        self.assertTrue(isinstance(first_item, ThriftyEnum))
        self.assertEqual("ProcessState", first_item.name)
        self.assertEqual(3, len(first_item.values))
        self.assertEqual("Just a simple enum.", first_item.comment)

        # ====================================================
        # Struct reading
        # ====================================================
        second_item: ThriftyStruct = model.file_items[1]
        self.assertTrue(isinstance(second_item, ThriftyStruct))
        self.assertEqual("ProcessResult", second_item.name)
        self.assertEqual("Just a very\nvery\nsimple struct.", second_item.comment)
        self.assertEqual(2, len(second_item.attributes))
        self.assertEqual("state", second_item.attributes[0].name)
        self.assertEqual("ProcessState", second_item.attributes[0].attrtype.name)
        self.assertEqual("exitCode", second_item.attributes[1].name)
        self.assertEqual("i32", second_item.attributes[1].attrtype.name)

        # ====================================================
        # Exception reading
        # ====================================================
        third_item: ThriftyException = model.file_items[2]
        self.assertTrue(isinstance(third_item, ThriftyException))
        self.assertEqual("ProcessError", third_item.name)
        self.assertEqual(2, len(third_item.attributes))
        self.assertEqual("message", third_item.attributes[0].name)
        self.assertEqual("string", third_item.attributes[0].attrtype.name)
        self.assertEqual("stack", third_item.attributes[1].name)
        self.assertEqual("string", third_item.attributes[1].attrtype.name)

        # ====================================================
        # Service reading
        # ====================================================
        fourth_item: ThriftyService = model.file_items[3]
        self.assertTrue(isinstance(fourth_item, ThriftyService))
        self.assertEqual("ProcessExecution", fourth_item.name)
        self.assertEqual(2, len(fourth_item.methods))

        # first method
        first_method = fourth_item.methods[0]
        self.assertEqual("Process the result", first_method.comment)
        self.assertEqual("processThing", first_method.name)
        self.assertEqual("ProcessResult", first_method.return_type.name)
        self.assertEqual(1, len(first_method.attributes))
        self.assertEqual(1, len(first_method.exceptions))

        # second method
        second_method = fourth_item.methods[1]
        self.assertEqual("Execute a thing on the server.", second_method.comment)
        self.assertEqual("executeThing", second_method.name)
        self.assertEqual("ProcessResult", second_method.return_type.name)
        self.assertEqual(2, len(second_method.attributes))
        self.assertEqual(1, len(second_method.exceptions))


if __name__ == '__main__':
    unittest.main()
