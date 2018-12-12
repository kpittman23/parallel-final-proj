import random, time, sys
from multiprocessing import Process, Pipe


def main():
    N = 2000000

    #copy list so it is same for sequential and parallel
    lystbck = [random.random() for x in range(N)]

    #Sequential quicksort a copy of the list.
    lyst = list(lystbck)            
    start = time.time()             
    lyst = quicksort(lyst)          
    elapsed = time.time() - start   
    
    if not isSorted(lyst):
        print('quicksort failed to sort the list')
        
    print('Sequential quicksort: %f sec' % (elapsed))

    
    time.sleep(3)
    
    #Parallel quicksort.
    lyst = list(lystbck)
    
    start = time.time()
    n = 3 #2**(n+1) - 1 processes will be instantiated.

    #Instantiate a Pipe so that we can receive the
    #process's response.
    pconn, cconn = Pipe()
    
    #Instantiate a process that executes quicksortParallel
    #on the entire list.
    p = Process(target=quicksortParallel, \
                args=(lyst, cconn, n))
    p.start()
    
    lyst = pconn.recv()
    #Blocks until there is something (the sorted list)
    #to receive.
    
    p.join()
    elapsed = time.time() - start

    if not isSorted(lyst):
        print('quicksortParallel failed to sort list')

    print('Parallel quicksort: %f sec' % (elapsed))


    time.sleep(3)
    
    #From github: Built-in test.
    #The underlying c code is obviously the fastest, but then
    #using a calculator is usually faster too.  That isn't the
    #point here obviously.
    lyst = list(lystbck)
    start = time.time()
    lyst = sorted(lyst)
    elapsed = time.time() - start
    print('Built-in sorted: %f sec' % (elapsed))

    
def quicksort(lyst):
    if len(lyst) <= 1:
        return lyst
    pivot = lyst.pop(random.randint(0, len(lyst)-1))
    
    return quicksort([x for x in lyst if x < pivot]) \
           + [pivot] \
           + quicksort([x for x in lyst if x >= pivot])

def quicksortParallel(lyst, conn, procNum):
    #Partition the list, then quicksort the left and right
    #sides in parallel.

    if procNum <= 0 or len(lyst) <= 1:
        #In the case of len(lyst) <= 1, quicksort will
        #immediately return anyway.
        conn.send(quicksort(lyst))
        conn.close()
        return

    #Create two independent lists (independent in that
    #elements will never need be compared between lists).
    pivot = lyst.pop(random.randint(0, len(lyst)-1))

    leftSide = [x for x in lyst if x < pivot]
    rightSide = [x for x in lyst if x >= pivot]

    pconnLeft, cconnLeft = Pipe()

    leftProc = Process(target=quicksortParallel, \
                       args=(leftSide, cconnLeft, procNum - 1))
    

    pconnRight, cconnRight = Pipe()
    rightProc = Process(target=quicksortParallel, \
                       args=(rightSide, cconnRight, procNum - 1))

    #Start
    leftProc.start()
    rightProc.start()

    #From github: Our answer is the concatenation of the subprocesses' 
    #answers, with the pivot in between. 
    conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
    conn.close()

    #Join
    leftProc.join()
    rightProc.join()

def isSorted(lyst):
    for i in range(1, len(lyst)):
        if lyst[i] < lyst[i-1]:
            return False
    return True


#Call the main method if run from the command line.
if __name__ == '__main__':
    main()