import os
# from __init__ import cfrate
import cfrate
class testing(cfrate):
    def __init__(self):
        super().__init__()
        print('base')

    def do(self):
        print('gotcha...')

    def change(self):
        os.system('color 03')

    def setup(self):
        print('working')
x = testing()
