from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.freq = defaultdict(int)  # word → frequency


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]
            node.freq[word] += 1  # track frequency at each prefix

        node.is_end = True

    def search(self, prefix: str, top_k: int = 5):
        node = self.root

        # Traverse the prefix
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Get top-k frequent words
        sorted_words = sorted(
            node.freq.items(),
            key=lambda x: -x[1]
        )

        return [word for word, _ in sorted_words[:top_k]]

    def update_frequency(self, word: str):
        """
        Call this when a user selects a suggestion.
        Boosts ranking.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return  # word not present

            node = node.children[char]
            node.freq[word] += 1

    

