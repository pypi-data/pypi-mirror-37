import os
import webbrowser
from cfrate import cfrate
def logger(func):
    name = func.__name__
    def wrapper(func):
        def call(*args,**krg):
            print(name)
            res=func(*args,**krg)
            return res
        return call
    return wrapper

class main_class(cfrate):
    def __init__(self):
        super().__init__()

    # @logger
    def readtxt(self):
        try:
            fi = open(self.file,'r')
            url = fi.read()
            fi.close()
            return url
        except Exception as ex:
            print('could\'nt find folder')
            return None

    # @logger
    def writetxt(self):
        fi  = open(self.file,'w')
        url = input("enter the link to tha page you want opened: ")
        print(url)
        print(url,file = fi)
        fi.close()
        return url

    # @logger
    def change(self):
        self.url = self.writetxt()

    # @logger
    def setup(self):
        self.file = "url.txt"
        print(self.path)
        path = self.path.split('\\')
        path.pop()
        self.path = '\\'.join(path)
        print(self.path)
        os.chdir(self.path)
        self.url = self.readtxt()
        if not self.url:
            self.url = self.writetxt()

    # @logger
    def do(self):
        webbrowser.open(self.url)
def main():
    main_class()
