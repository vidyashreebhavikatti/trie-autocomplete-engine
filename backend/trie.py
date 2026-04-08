from collections import defaultdict


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.freq = defaultdict(int)


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.all_words = set()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.freq[word] += 1
        node.is_end = True
        self.all_words.add(word)

    def search(self, prefix: str, top_k: int = 5):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        sorted_words = sorted(
            node.freq.items(),
            key=lambda x: -x[1]
        )
        return [word for word, _ in sorted_words[:top_k]]

    def search_with_typos(self, prefix: str, max_distance: int = 2, top_k: int = 5):
        if not prefix:
            return []
        
        candidates = []
        
        for word in self.all_words:
            if abs(len(word) - len(prefix)) > max_distance:
                continue
            
            if word.startswith(prefix):
                distance = len(word) - len(prefix)
            else:
                distance = levenshtein_distance(prefix, word)
            
            if distance <= max_distance:
                freq = self._get_frequency(word)
                score = (max_distance - distance + 1) * 1000 + freq
                candidates.append((word, score, distance))
        
        candidates.sort(key=lambda x: (-x[1], x[2]))
        return [word for word, _, _ in candidates[:top_k]]
    
    def _get_frequency(self, word: str) -> int:
        return self.root.freq.get(word, 0)

    def update_frequency(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                return
            node = node.children[char]
            node.freq[word] += 1