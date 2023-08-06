from cfrate import *
import os
def main():
    platform =  os.sys.platform.lower()
    if not 'win' in platform:
        from cfrate.filehandles import main
        main()
    else:
        from cfrate.browserhandles import main
        main()
