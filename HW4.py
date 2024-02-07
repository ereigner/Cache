# HW4

class Node:
    def __init__(self, content):
        self.value = content
        self.next = None
        self.previous = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    '''
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1005, 18, "another header", "111110")
        >>> hash(content1)
        0
        >>> hash(content2)
        1
        >>> hash(content3)
        2
        >>> hash(content4)
        1
    '''
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        sum = 0
        for item in self.header:                    # Iterates through the string in self.header
            sum += ord(item)                        # Adds the ASCII value of the string value to sum
        return sum%3                                # Returns the sum modulus 3




class CacheList:
    '''
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 180, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1006, 18, "another header", "111110")
        >>> content5 = ContentItem(1008, 2, "items", "11x1110")
        >>> lst=CacheList(200)
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> lst.put(content2, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> lst.put(content4, 'mru')
        'INSERTED: CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110'
        >>> lst
        REMAINING SPACE:122
        ITEMS:3
        LIST:
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        >>> lst.put(content5, 'mru')
        'INSERTED: CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110'
        >>> lst
        REMAINING SPACE:120
        ITEMS:4
        LIST:
        [CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        >>> lst.put(content3, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> lst
        REMAINING SPACE:0
        ITEMS:3
        LIST:
        [CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>]
        [CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        <BLANKLINE>
        >>> lst.tail.value
        CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110
        >>> lst.tail.previous.value
        CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110
        >>> lst.tail.previous.previous.value
        CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>
        >>> lst.tail.previous.previous is lst.head
        True
        >>> lst.tail.previous.previous.previous is None
        True
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        [CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        <BLANKLINE>
        >>> 1006 in lst
        True
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        [CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110]
        <BLANKLINE>
        >>> contentExtra = ContentItem(1034, 2, "items", "other content")
        >>> lst.update(3000, contentExtra)
        'Cache miss!'
        >>> lst.update(1008, contentExtra)
        'UPDATED: CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content'
        >>> 1008 in lst
        False
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        
        >>> contentExtraDiff = ContentItem(1504, 150, "more items", "other content")
        >>> lst.update(1006, contentExtraDiff)
        'UPDATED: CONTENT ID: 1504 SIZE: 150 HEADER: more items CONTENT: other content'
        >>> lst
        REMAINING SPACE:38
        ITEMS:3
        LIST:
        [CONTENT ID: 1504 SIZE: 150 HEADER: more items CONTENT: other content]
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>

        >>> contentExtraMore = ContentItem(2504, 50, "other items", "other content")
        >>> lst.update(1000, contentExtraMore)
        'Cache miss!'
        >>> lst
        REMAINING SPACE:38
        ITEMS:3
        LIST:
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        [CONTENT ID: 1504 SIZE: 150 HEADER: more items CONTENT: other content]
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        <BLANKLINE>

    
        >>> lst.clear()
        'Cleared cache!'
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
    '''
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        return self.numItems
    
    def put(self, content, evictionPolicy):
        if content.size > self.maxSize:
            return 'Insertion not allowed'
        if self.__contains__(content.cid) == True:                                  #If the new content ID exists in the list currently return True from contains 
            return f'Content {content.cid} already in cache, insertion not allowed'
        else:
            if evictionPolicy == 'mru':                             #If the eviction Policy is 'mru' then continue to remove items until the content is smaller than remaining space
                while content.size > self.remainingSpace:
                    self.mruEvict()
            if evictionPolicy == 'lru':
                while content.size > self.remainingSpace:           #If the eviction Policy is 'lru' loop until content is smaller than remaining space
                    self.lruEvict()
            if self.head == None:                                   # if there is nothing in the list just add the node like usual
                nn = Node(content)
                self.head = nn                              
                self.tail = nn
                self.remainingSpace -= nn.value.size
                self.numItems += 1
                return f'INSERTED: {content}'
            else:                                                   # Adds the node to the beginning of the list contenting pointer correctly
                nn = Node(content)
                nn.next = self.head
                self.head.previous = nn
                self.head = nn
                self.remainingSpace -= nn.value.size
                self.numItems += 1
                return f'INSERTED: {content}'


    

    def __contains__(self, cid):
        if self.head == None:                               # if the list is empty return False
            return False
        if self.head.value.cid == cid:                      # If the head CID matches the one given return True
            return True
        elif self.tail.value.cid == cid:                    # If the tail CID matches the one given unlink the tail node and move to the front
            temp = self.tail                                
            temp.previous.next = None                       # Unlinks the previous nodes pointer to None
            self.tail = temp.previous                       # Tails moves to previous node
            temp.previous = None                            # temp now does not point previous to tail
            temp.next = self.head                           # Points temp to the head node
            self.head.previous = temp                       # Head previously points to temp
            self.head = temp                                # The head is now temp
            return True
        else:                                                   # If the node is in the middle you have to do unlinking from two nodes and then add it to the front
            current = self.head
            while current.next is not None:                     # Loops through until the end
                if current.value.cid == cid:                    # Looks for if a node's cid matches with the new cid
                    current.next.previous = current.previous    
                    current.previous.next = current.next        # Sets the previous nodes next pointer to the node current points to
                    current.previous = None                     
                    current.next = self.head                    
                    self.head.previous = current                # Sets the heads previous pointer to current
                    self.head = current                         
                    return True
                current = current.next                          # Moves to the next node
            return False




    def update(self, cid, content):
        if content.size > self.maxSize:                                      
            return 'Cache miss!'
        if self.__contains__(cid) == True:                                      # Goes through contains and if it is true it continues
            if self.remainingSpace + self.head.value.size > content.size:       # If remainingspace + the value now moved to the top is greater than content size continue
                self.remainingSpace -= content.size - self.head.value.size      # Subtracts remaining space from the new content size minus the head values size
                self.head.value = content
                return f'UPDATED: {content}'
        return 'Cache miss!'
            


    def mruEvict(self):
        if self.head is not None:
            temp = self.head                                        # Stores the heads node into temp to use later
            self.head = self.head.next                              # Makes the head now the next node using the heads pointer
            temp.next = None                                        # Makes the original node point to None                               # Makes the new head's value point backwards to none
            self.numItems -= 1
            self.remainingSpace += temp.value.size

    
    def lruEvict(self):
        if self.__len__() == 1:
            self.clear()
        else:
            temp = self.tail                                        # Sets the tail to a temp variable
            temp.previous.next = None                               # Sets the previous of tail pointing to the next to None           
            self.tail = temp.previous                               # temps previous value is now the tail
            temp.previous = None                                    # Removes the pointer to the tail
            self.numItems -= 1
            self.remainingSpace += temp.value.size

    
    def clear(self):
        if self.head == None:
            return 'Cleared cache!'
        else:
            while self.head is not None:                            # Continues to remove the head node until there are no nodes left
                self.mruEvict()
            return 'Cleared cache!'


class Cache:
    """
        # An extended version available on Canvas. Make sure you pass this doctest first before running the extended version

        >>> cache = Cache()
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")

        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")

        >>> content7 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")

        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed'

        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'

        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:177
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:45
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:16
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache[content9].next.value
        CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>
    """

    def __init__(self):
        self.hierarchy = [CacheList(200), CacheList(200), CacheList(200)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__


    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    
    def insert(self, content, evictionPolicy):
        return self.hierarchy[hash(content)].put(content, evictionPolicy)                   # Returns the hashed value to decide which list it goes into and then calls the put function to put inside hierarchy


    def __getitem__(self, content):
        if self.hierarchy[hash(content)].__contains__(content.cid):                         # If hierarchy already has the content it will return the head node. Else Return 'Cache miss!'
            return self.hierarchy[hash(content)].head                                       
        else:
            return 'Cache miss!'



    def updateContent(self, content):
        return self.hierarchy[hash(content)].update(content.cid, content)                   # Returns hierarchy with the correct hashed content after going through the update function in cachelist


if __name__ == '__main__':
    import doctest
    doctest.run_docstring_examples(CacheList, globals(), name='LAB5',verbose=True)


   
