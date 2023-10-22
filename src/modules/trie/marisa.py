from marisa_trie import RecordTrie
from typing import Any, Generator, List, Tuple
from src.modules.trie.base import Trie, TrieQuery
from src.modules.wordlist.wordlist import WordList
from src.modules.trie.loader import word_iter


class MarisaTrie(Trie):

    def __init__(self) -> None:
        self.trie: RecordTrie = None
        self.words: List[str] = []

    def insert_trie(self, loader: WordList) -> None:
        ind: int = 0
        trie_keys: List[str] = []
        trie_data: List[Tuple[int]] = []

        for word in loader.get_words():
            for iword in word_iter(word):
                trie_keys.append(iword)
                trie_data.append((ind,))

            self.words.append(word)
            ind += 1
        self.trie = RecordTrie("<i", zip(trie_keys, trie_data))
    
    def query_trie(self) -> TrieQuery:
        return MarisaTrieQuery(self)


class MarisaTrieQuery(TrieQuery):

    def __init__(self, trie: Trie) -> None:
        self.trie: MarisaTrie = trie
    
    def get_status(self) -> Any:
        return None

    def get_key(self, status: Any, word: str) -> Tuple[Any, str]:
        return status, self.trie.trie.has_keys_with_prefix(word)

    def get_leaf(self, status: Any, word: str) -> Generator[str, None, None]:
        for i in self.trie.trie.get(word, []):
            yield self.trie.words[i[0]]
