#BY : theUnderdog
#-----------------
def main():
##settings
    file = 'so.mp3' #the name of the file to played as an alert.
    secs = 120      #the number of seconds between each request.
    ##end of settings
    import requests
    from time import sleep,ctime
    import os
    id=os.sys.argv[1]  #contest ID
    url  = f'http://codeforces.com/api/contest.ratingChanges?contestId={id}'
    import sys
    def progress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()
    def get(id,handle=None):
        '''
            if a handle is given the the Program will output the rate change of that
            handle.
            otherwise you be given an alert that the rating for all participants has
            changed
        '''
        try:
            print(f'sending {id}, {handle if handle else ""} , {ctime()} ...')
            res = requests.get(url).json()
            if res['status']!='FAILED' and len(res['result']):
                ## for linux this should be changed to the right command -which I don't know
                os.system(f'start {file}')
                if handle:
                    for result in res['result']:
                        if result['handle'].lower()==handle:
                            old = result['oldRating']
                            new = result['newRating']
                            print(f'gain : {new-old}\n{old} -> {new}')
                            break
                    else:
                        print(f'couldn\'t find this handle ->{handle}')
                quit()
            for i in range(secs):
                sleep(1)
                progress(i, secs, status='Before next Request')
            get(id,handle)
        except Exception as ex:
            print('wrong ', ex)
            get(id,handle)
    if len(os.sys.argv)==3:
        handle = os.sys.argv[2].lower()
        get(id,handle)
    else:
        get(id)
