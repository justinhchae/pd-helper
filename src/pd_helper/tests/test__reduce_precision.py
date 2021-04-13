from unittest import TestCase


class Test(TestCase):
    from src.pd_helper.tests.test__config import FakeDF

    df = FakeDF().df
    _reduce_precision = FakeDF()._reduce_precision_

    def test__reduce_precision_string(self):

        s = Test._reduce_precision(Test.df["Object ID"])
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'string')

    def test__reduce_precision_category(self):
        s = Test._reduce_precision(Test.df["Item Name"])
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'category')

    def test__reduce_precision_datetime(self):
        s = Test._reduce_precision(Test.df["Retrieved Date"])
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'datetime64[ns]')

    def test__reduce_precision_boolean(self):
        s = Test._reduce_precision(Test.df["Retrieved"])
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'boolean')

    def test__reduce_precision_int8(self):
        s = Test._reduce_precision(Test.df["Sector"])
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'int8')

    def test__reduce_precision_float16(self):
        s = Test._reduce_precision(Test.df["Weight"])
        data_type = str(s.dtype)
        self.assertEqual(data_type, 'float16')
