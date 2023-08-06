import requests
from time import sleep,ctime
import os
import sys
class cfrate:
    def __init__(self):
        #general info
        self.path   = os.path.abspath(__file__)
        self.secs   = 120
        self.id     = os.sys.argv[1]
        self.__url    = f'http://codeforces.com/api/contest.ratingChanges?contestId={self.id}'
        self.handle = None
        if len(os.sys.argv)==3:
            self.handle = os.sys.argv[2].lower()
        self.setup()
        if self.id == '-1':
            self.change()
            quit()
        self.get()

    def setup(self):
        """
        To be overriden in the derivative class
        called before the the requests strart to
        setup every thing.
        """
        pass
    def change(self):
        """
        To be overriden in the derivative class
        called when ID == -1 in order to
        change the genral info or previous setup
        """
        pass

    def do(self):
        """
        To be overriden in the derivative class
        contains the code you want to execute once
        the requests comes in.

        """
    def progress(self,count,total,status=''):
        '''
        used to handle the progress bar
        '''
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()



    def get(self):
        '''
        a recursive function where the magic happens
        if a handle is given the program will get
        the change in that handle rate.
        '''
        try:
            print(f'sending {self.id}, {self.handle if self.handle else ""} , {ctime()} ...')
            res = requests.get(self.__url).json()
            if res['status']!='FAILED' and len(res['result']):
                self.do()
                if self.handle:
                    for result in res['result']:
                        if result['handle'].lower()==self.handle:
                            old = result['oldRating']
                            new = result['newRating']
                            print(f'gain : {new-old}\n{old} -> {new}')
                            break
                    else:
                        print(f'couldn\'t find this handle ->{self.handle}')
                quit()
            for i in range(self.secs):
                sleep(1)
                self.progress(i, self.secs, status='Before next Request')
            self.get()
        except Exception as ex:
            print('cfrate wrong', ex)
            # self.get()

