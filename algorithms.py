# returns the most common value for that key
def most_common(L):
    return max(set(L), key=L.count)
    

class FBABallot:
    def __init__(self):
        self.map = dict()

    def append(self, key, value):
        if key not in self.map:
            self.map[key] = list()
        
        self.map[key].append(value)

    def most_often(self, key):
        if key in self.map:
            return most_common(self.map[key])
        else:
            raise Exception("Key not in map")

    def get(self, key):
        return self.map[key]

    def keys(self):
        return self.map.keys()

    def snapshot(self):
        return self.map


if __name__ == '__main__':

    manager = FBABallot()

    manager.append('hello', 'world')
    manager.append('hello', '123')
    manager.append('hello', '123')
    

    print(manager.snapshot())
    print(manager.most_often('hello'))