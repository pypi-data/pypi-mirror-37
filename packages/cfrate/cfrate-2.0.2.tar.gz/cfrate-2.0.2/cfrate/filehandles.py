import os
import time
def track(fun):
        # print(fun.__name__)
        pass
class FileHandler:
    def __init__(self,path):
        path = path.split('\\')
        path.pop()
        path = '\\'.join(path)
        self.path = path
        self.validextentios = ['.mp3','.mp4']
        self.foldername = 'mediaFolder'


    def checkPath(self,path):
        track(self.checkPath)
        return os.path.isdir(path)

    def getsong(self,path):
        track(self.getsong)
        for fi in os.listdir(path):
            for ext in self.validextentios:
                if fi.endswith(ext):
                    return fi
        else:
            return False
            # raise Exception "no file not found"
    def createFolder(self):
        track(self.createFolder)
        os.mkdir(self.folderpath)

    def openFolder(self):
        track(self.openFolder)
        os.system(f'explorer {self.folderpath}')

    def core(self,add = False):
        track(self.core)
        self.folderpath = f'{self.path}\\{self.foldername}'
        fp=self.folderpath
        if self.checkPath(fp) and not add:
            os.chdir(fp)
            oso = self.getsong(fp)
            so = ''.join(oso.split())
            os.rename(oso,so)
            print(so)
            if so:
                return so
            else:
                print('you need to add a media file first...')
                print('then tun the program again')
                time.sleep(1)
                self.openFolder()
                quit()
        if not self.checkPath(fp):
            self.createFolder()
            add  = True
        if add:
            print('you need to add a media file first...')
            print('then tun the program again')
            self.openFolder()
            quit()











