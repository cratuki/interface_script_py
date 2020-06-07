import unittest

from interface_script import InterfaceScriptParser
from interface_script import SignalConsumer

SAMPLE = '''
i person name age
i org name

person jane 35
person maria 45

org "Southwark and Vauxhall Waterworks Company"
org "New River Company" # comment
'''

class TestBasics(unittest.TestCase):

    def test_simple(self):
        acc = []
        class SampleSC(SignalConsumer):
            def on_person(self, name, age):
                acc.append("%s/%s"%(name, age))
            def on_org(self, name):
                acc.append(name)

        signal_consumer = SampleSC()
        ob = InterfaceScriptParser(
            cb_interface=signal_consumer.on_interface,
            cb_signal=signal_consumer.on_signal)
        ob.parse(SAMPLE)
        assert len(acc) == 4
        assert acc[0] == "jane/35"
        assert acc[-1] == "New River Company"
        return True


if __name__ == '__main__':
    unittest.main()
