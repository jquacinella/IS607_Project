# simple CSV exporter
import sys
from PyDTA import Reader

dta = Reader(file("snap/qcfy2011.dta"))

for observation in dta.dataset():
    print ",".join(map(str,observation))