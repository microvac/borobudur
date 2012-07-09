import peppercorn
from peppercorn import START, END, MAPPING, SEQUENCE

fields = [
    ['name', 'project1'],
    ['title', 'Cool project'],
    [START, 'series:%s' % MAPPING],
    ['name', 'date series 1'],
    [START, 'dates:%s' % SEQUENCE],
    [START, 'date:%s' % SEQUENCE],
    ['day', '10'],
    ['month', '12'],
    ['year', '2008'],
    [END, 'date:%s' % SEQUENCE],
    [START, 'date:%s' % SEQUENCE],
    ['day', '10'],
    ['month', '12'],
    ['year', '2009'],
    [END, 'date:%s' % SEQUENCE],
    [END, 'dates:%s' % SEQUENCE],
    [END, 'series:%s' % MAPPING],
]

parsed = peppercorn.parse(fields)
print parsed["series"]["dates"][0][0]
print parsed["series"]["dates"][0][2]
print parsed["name"]

