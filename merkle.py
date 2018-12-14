def print_tree(self, hash):
        value = self._transactions[hash]
        # TODO
        item =value[0]
        child = value[1]
        print(hash, item)
        if not child:
            return
        for hashitem, item in child.items():  
            print ("    -> %s %s" % (hashitem, item))
        for hashitem, item in child.items():  
            self.print_tree(hashitem)

def find_diff(merkle_tree_a, a_roothash, merkle_tree_b, b_roothash):
    if a_roothash == b_roothash:
        print("Top hash is equal for %s and %s" % (merkle_tree_a._rootDir, merkle_tree_b._rootDir))
    else:
        a_value = merkle_tree_a._transactions[a_roothash] 
        a_child = a_value[1]    # retrieve the child list for merkle tree a
        b_value = merkle_tree_b._transactions[b_roothash] 
        b_child = b_value[1]    # retrieve the child list for merkle tree b

        # TODO 
        for hashitem, item in a_child.items():
            try:
                if b_child[hashitem] == item:
                    print ("SAME: %s" % item)
            except KeyError:
                
                    print ("DIFF: %s" % item)
                    temp_value = merkle_tree_a._transactions[hashitem]
                    if len(temp_value[1]) > 0:    
                        diffhash = list(set(b_child.keys()) - set(a_child.keys()))
                        find_diff(merkle_tree_a, hashitem, merkle_tree_b, diffhash[0])
                    
             
