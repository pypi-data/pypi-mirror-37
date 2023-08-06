from cfrate import *
import os
def main():
    platform =  os.sys.platform.lower()
    if 'win' in platform:
        from cfrate.filehandles import main
        main()

