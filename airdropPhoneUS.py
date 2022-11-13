import time
import hashlib
import multiprocessing as mp
targetstart = '3bbc8'#input('Enter the target hash start fragment: ')
targetend = '844e6'#input('Enter the target hash end fragment: ')
areacodelist = list(range(646,650))
phonematch = mp.Manager().list()

def checkPhoneNumber(areacode):
    # global phonematch
    ts = time.time()
    line = '0'
    print('Searching area code', str(areacode), 'for target...')
    while int(line) < 10000000:
        targetphone = '1' + str(areacode) + str(line).zfill(7)
        targettest = hashlib.sha256(targetphone.encode())
        starthashcheck = targettest.hexdigest() [0:5]
        endhashcheck = targettest.hexdigest() [-5:]
        if starthashcheck == targetstart.lower() and endhashcheck == targetend.lower():
            print('===================================================================')
            print('!', targetphone, 'matches hash fragments. Still checking for others...')
            print('===================================================================')
            phonematch.append(targetphone)
        line = int(line) + 1
    print('Finished searching area code', str(areacode), 'with time {:.2f} s'.format(time.time()-ts))

if __name__ == '__main__':
    print('Checking all area codes in North America. Results will report on completion.')
    t0 = time.time()
    cores = mp.cpu_count()
    print('Cores:', cores)
    pool = mp.Pool(processes=cores)
    pool.map(checkPhoneNumber,areacodelist)
    pool.close()
    pool.join()
    
    if phonematch:
        print('\nYour target\'s phone number may be:')
        print(phonematch)
#         for match in phonematch:
#             print(match)
    else:
        print('\nTarget phone number not found in this area code set. Target phone may use another country code.')

    print('\nAll time: {:.2f} s'.format(time.time()-t0))
