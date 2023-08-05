from helper.parse import parser
import unittest

class TestStringMethods(unittest.TestCase):
    def test_parser(self):
        self.assertEqual(parse('<!DOCTYPE html><html><body><h2>Basic HTML Table</h2>'+
           '<table><tr><th>Firstname</th><th>Lastname</th>'+ 
           '<th>Age</th></tr><tbody><tr><td>Jill</td><td>Smith</td><td>50</td></tr>'+
           '</tbody></table></body></html>'), [['Firstname', 'Lastname', 'Age'], ['Jill', 'Smith', 50]])
