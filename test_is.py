import unittest

from interface_script import InterfaceScriptParser

SAMPLE = '''
i person name age
i org name

person jane 35
person maria 45

org "Southwark and Vauxhall Waterworks Company"
org "New River Company" # comment
'''

class Handler:

    def __init__(self):
        self.acc = []

    def on_person(self, name, age):
        self.acc.append("%s/%s"%(name, age))

    def on_org(self, name):
        self.acc.append(name)


class TestBasics(unittest.TestCase):

    def test_simple(self):
        handler = Handler()

        ob = InterfaceScriptParser(handler)
        ob.parse(SAMPLE)

        # Validate
        acc = handler.acc
        assert len(acc) == 4
        assert acc[0] == "jane/35"
        assert acc[-1] == "New River Company"

        return True


if __name__ == '__main__':
    unittest.main()
