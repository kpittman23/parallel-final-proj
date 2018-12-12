from multiprocessing import Pool
import time, random, sys

#Dependencies defined below main()

def main():

    N = 2000000

    lystbck = [random.random() for x in range(N)]

    lyst = list(lystbck)
    start = time.time()             
    lyst = mergesort(lyst)
    elapsed = time.time() - start   

    if not isSorted(lyst):
        print('Sequential mergesort did not sort. oops.')
    
    print('Sequential mergesort: %f sec' % (elapsed))


    
    time.sleep(3)


     
    lyst = list(lystbck)
    start = time.time()
    n = 3 #2**(n+1) - 1 processes will be instantiated.

    lyst = mergeSortParallel(lyst, n)

    elapsed = time.time() - start

    if not isSorted(lyst):
        print('mergeSortParallel did not sort. oops.')

    print('Parallel mergesort: %f sec' % (elapsed))


    time.sleep(3)
    
    lyst = list(lystbck)
    start = time.time()
    lyst = sorted(lyst)
    elapsed = time.time() - start
    print('Built-in sorted: %f sec' % (elapsed))


def merge(left, right):
    ret = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] <= right[ri]:
            ret.append(left[li])
            li += 1
        else:
            ret.append(right[ri])
            ri += 1
    if li == len(left):
        ret.extend(right[ri:])
    else:
        ret.extend(left[li:])
    return ret

def mergesort(lyst):

    if len(lyst) <= 1:
        return lyst
    ind = len(lyst)//2
    return merge(mergesort(lyst[:ind]), mergesort(lyst[ind:]))

def mergeWrap(AandB):
    a,b = AandB
    return merge(a,b)

def mergeSortParallel(lyst, n):

    numproc = 2**n
    #Evenly divide the lyst indices.
    endpoints = [int(x) for x in linspace(0, len(lyst), numproc+1)]
    #partition the lyst.
    args = [lyst[endpoints[i]:endpoints[i+1]] for i in range(numproc)]

    pool = Pool(processes = numproc)
    sortedsublists = pool.map(mergesort, args)

    while len(sortedsublists) > 1:
        args = [(sortedsublists[i], sortedsublists[i+1]) \
				for i in range(0, len(sortedsublists), 2)]
        sortedsublists = pool.map(mergeWrap, args)

    return sortedsublists[0]
    

    
def linspace(a,b,nsteps):
    """
    returns list of simple linear steps from a to b in nsteps.
    """
    ssize = float(b-a)/(nsteps-1)
    return [a + i*ssize for i in range(nsteps)]


def isSorted(lyst):
    for i in range(1, len(lyst)):
        if lyst[i] < lyst[i-1]:
            return False
    return True

if __name__ == '__main__':
    main()