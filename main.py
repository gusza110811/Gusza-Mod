# Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn
# See C.txt

from compat_fix import *
from engine import *
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


if __name__ == "__main__":
    clear()
    print('Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn\n\n')

    menu.main()