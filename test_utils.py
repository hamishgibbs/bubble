from utils import language

class TestLanguage():
    '''Test language extraction from file extansion'''

    def test_language_r(self):
        '''Test language extraction from R file'''

        path = 'file.R'

        assert language(path) == 'R'

    def test_language_py(self):
        '''Test language extraction from Python file'''

        path = 'file.py'

        assert language(path) == 'PYTHON'

    def test_language_abs(self):
        '''Test language extraction from absolute path file'''

        path = '/usr/anyone/file.R'

        assert language(path) == 'R'
