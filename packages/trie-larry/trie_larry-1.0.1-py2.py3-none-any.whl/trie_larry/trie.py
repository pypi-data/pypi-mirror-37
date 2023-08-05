
class Trie:
    def __init__(self):
        self.root = {}
        self.word_end = -1

    def insert(self, word):
        cur_node = self.root
        for c in word:
            if not c in cur_node:
                cur_node[c] = {}
            cur_node = cur_node[c]
        cur_node[self.word_end] = True
    def search(self, word):
        cur_node = self.root
        for c in word:
            if not c in cur_node:
                return False
            cur_node = cur_node[c]

        if self.word_end not in cur_node:
            return False
        return True
