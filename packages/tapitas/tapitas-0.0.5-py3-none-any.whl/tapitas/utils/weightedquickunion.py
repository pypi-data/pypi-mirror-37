
## author: benny chin @ 2015/12/02 ##
## a generic class for weighted quick union implementation ##
# lists of string, integer are tested...
# a lookup dictionary is used for identifying item from the "simple list", which record the root of the item at the index

class GenericWeightedQuickUnion():
    def __init__(self, init_list=[]):
        self._roots = [] ## parent (position as in the init_list)
        self.lookuptable = {} ## dict(item = position in init_list)
        self.sizes = [] ## child size(position as in the init_list)
        self.item_list = [] ## item (position as in the init_list)
        for i in range(len(init_list)):
            self.lookuptable[init_list[i]] = i
            self._roots.append(i)
            self.sizes.append(1)
            self.item_list.append(init_list[i])

    def additem(self, item):
        j = len(self._roots)
        self.lookuptable[item] = j
        self._roots.append(j)
        self.sizes.append(1)
        self.item_list.append(item)

    def union(self, item_p, item_q):
        p = self.lookuptable[item_p]
        q = self.lookuptable[item_q]
        self._union(p, q)

    def _union(self, p, q):
        i = self._findroot(p)
        j = self._findroot(q)
        if i != j:
            sz_i = self.sizes[i]
            sz_j = self.sizes[j]
            if ( sz_i < sz_j ): # a speed up move
                self._roots[i] = j
                self.sizes[j] = sz_i+sz_j
            else:
                self._roots[j] = i
                self.sizes[i] = sz_i+sz_j

    def findroot(self, item_k):
        k = self.lookuptable[item_k]
        return self._findroot(k)

    def _findroot(self, k):
        r = k
        while (r != self._roots[r]):
            r = self._roots[r]
        self._roots[k] = r # a speed up move
        return r

    def isconnected(self, item_p, item_q):
        return self._isconnected(self.lookuptable[item_p], self.lookuptable[item_q])

    def _isconnected(self, p, q):
        return self._findroot(p) == self._findroot(q)

    def get_currentcomponents(self, form='list'):
        root_dict = {}
        for i in range(len(self._roots)):
            kp = self._roots[i] # parent of item_k
            item_k = self.item_list[i]
            top_root = self._findroot(kp)
            if top_root not in root_dict:
                root_dict[top_root] = []
            root_dict[top_root].append(item_k)
        if form == 'dict':
            return root_dict
        elif form == 'list':
            # re-index the id of component
            #components = {}
            components_list = []
            keys = sorted(root_dict.keys())
            for i in range(len(keys)):
                #components[i] = root_dict[keys[i]]
                components_list.append(root_dict[keys[i]])
            return components_list
        else:
            print("not reconized 'form', returning list")
            # re-index the id of component
            #components = {}
            components_list = []
            keys = sorted(root_dict.keys())
            for i in range(len(keys)):
                #components[i] = root_dict[keys[i]]
                components_list.append(root_dict[keys[i]])
            return components_list



## for testing purpose: items of objects
class node():
    def __init__(self, key):
        self.id = key

## for analyzing running time ##
class analysis_of_timerunning():
    def __init__(self):
        import time
        times = []
        klist = []
        k = 2
        for i in range(10):
            k = k*2
            klist.append(k)
            print(k)
            starttime = time.time()
            self.running(k)
            stoptime = time.time()
            times.append(stoptime - starttime)
        import matplotlib.pyplot as plt
        #fig = plt.Figure()
        #ax = fig.add_subplot(1,1,1)
        plt.loglog(klist, times, basex=2)
        plt.show()

    def running(self, k):
        #k=10000
        dlist = [ node(i) for i in range(k) ]
        wqu4 = GenericWeightedQuickUnion(dlist)
        for i in range(int(k/2-1)):
            wqu4.union( dlist[i], dlist[i+1] )
        for i in range(int(k/2-1)):
            wqu4.union( dlist[int(i+k/2)], dlist[int(i+k/2+1)] )
        print(wqu4.isconnected( dlist[0], dlist[k-1] ))
        wqu4.union(dlist[int(k/2-1)], dlist[int(k/2)])
        print(wqu4.isconnected( dlist[0], dlist[k-1] ))



if __name__ == '__main__':
    """
    print ('===========test 1===========')
    alist = ['a','b','c','d','e','f','g','h']
    wqu = GenericWeightedQuickUnion(alist)
    wqu.union('a','b')
    print wqu.isconnected('a','b')
    print wqu.isconnected('a','c')
    wqu.union('g','h')
    wqu.union('b','c')
    print wqu.isconnected('e','a')
    wqu.union('e','h')
    wqu.union('h','b')
    print wqu.isconnected('e','a')


    print ('===========test 2===========')
    blist = [1,2,3,4,5,6,7,8]
    wqu2 = GenericWeightedQuickUnion(blist)
    wqu2.union(1,2)
    print wqu2.isconnected(1,2)
    print wqu2.isconnected(1,8)
    wqu2.union(2,4)
    wqu2.union(8,7)
    print wqu2.isconnected(1,8)
    wqu2.union(4,7)
    print wqu2.isconnected(1,8)


    print ('===========test 3===========')
    clist = [ node(i) for i in range(10) ]
    wqu3 = GenericWeightedQuickUnion(clist)
    wqu3.union( clist[1], clist[2] )
    print wqu3.isconnected(clist[1], clist[2])
    print wqu3.isconnected(clist[1], clist[9])
    wqu3.union( clist[2], clist[5])
    wqu3.union( clist[5], clist[9])
    print wqu3.isconnected(clist[1], clist[9])
    xxx = node(11)
    wqu3.additem(xxx)
    print wqu3.isconnected(clist[1], xxx )
    wqu3.union( clist[1], xxx )
    print wqu3.isconnected(clist[1], xxx )
    """

    print ('===========test 4===========')
    #import sys
    #print(sys.version)
    analysis_of_timerunning()
