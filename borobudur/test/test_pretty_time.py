import unittest
import translationstring
from borobudur.util.pretty_time import pretty_time
from datetime import datetime, timedelta

translator = translationstring.Translator()

class TestPrettyTime(unittest.TestCase):

    def setUp(self):
        pass

    def print_report(self, dt):
        print "Now       : " + datetime.now().strftime("%c")
        print "Test time : " + dt.strftime("%c")
        print pretty_time(dt, translator)

    def test_second(self):
        print "==========="
        print "TEST SECOND"
        print "==========="
        dt = datetime.now()
        self.print_report(dt)

    def test_minute(self):
        print "==========="
        print "TEST MINUTE"
        print "==========="
        dt = datetime.now() - timedelta(minutes=3)
        self.print_report(dt)

    def test_hour(self):
        print "========="
        print "TEST HOUR"
        print "========="
        dt = datetime.now() - timedelta(hours=2)
        self.print_report(dt)

    def test_one_day(self):
        print "============"
        print "TEST ONE DAY"
        print "============"
        dt = datetime.now() - timedelta(days=1)
        self.print_report(dt)

    def test_one_year(self):
        print "============="
        print "TEST ONE YEAR"
        print "============="
        dt = datetime.now() - timedelta(days=63)
        self.print_report(dt)

    def test_more_year(self):
        print "============="
        print "TEST > 1 YEAR"
        print "============="
        dt = datetime.now() - timedelta(days=760)
        self.print_report(dt)