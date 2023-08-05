
from helper.create import makeFile
import filecmp

class TestM1(unittest.TestCase):
    def test_make(self):
        data = [['Firstname', 'Lastname', 'Age'], ['Jill', 'Smith', 50]]
        makeFile('tester.csv', data)
        file1 = open('tester.csv', 'r') 
        file2 = open('test.csv', 'r')
        
        self.assertEqual(file1.read(), file2.read())
        
        file1.close()
        file2.close()
