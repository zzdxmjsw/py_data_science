from WindPy import *

w.start()
test = w.wsd('600000.SH', 'open', '2013050 6')

'''df = w.edb(
    "M5765840,M5765841,M5765842,M5765843,M5765844,M5765845",
    "2015-08-01",
    "2017-09-18",
    "Fill=Previous")'''

df = w.edb("M5765840,M5765845", "2016-01-01", "2017-09-18", "Fill=Previous")
