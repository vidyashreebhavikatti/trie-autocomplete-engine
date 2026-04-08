from trie import Trie

def load_words(trie):
    words = [
        "apple", "app", "apex", "application", "apply",
        "bat", "ball", "batter", "battle",
        "cat", "call", "camel", "camera", "care"
    ]
    for word in words:
        trie.insert(word)


def run_autocomplete():
    trie = Trie()
    load_words(trie)
    
    print("🔍 Smart Autocomplete with Typo Tolerance\n")
    print("Commands: 'fuzzy' to toggle fuzzy search, 'exit' to quit\n")
    
    fuzzy_mode = False
    
    while True:
        prefix = input("Enter prefix: ").strip().lower()
        
        if prefix == "exit":
            print("Goodbye!")
            break
        
        if prefix == "fuzzy":
            fuzzy_mode = not fuzzy_mode
            mode = "ON" if fuzzy_mode else "OFF"
            print(f"Fuzzy search: {mode}\n")
            continue
        
        if fuzzy_mode:
            suggestions = trie.search_with_typos(prefix, max_distance=2, top_k=5)
        else:
            suggestions = trie.search(prefix, top_k=5)
        
        if not suggestions:
            if not fuzzy_mode:
                suggestions = trie.search_with_typos(prefix, max_distance=2, top_k=5)
                if suggestions:
                    print("(Showing fuzzy matches)")
            
            if not suggestions:
                print("No suggestions found.\n")
                continue
        
        print("\nSuggestions:")
        for i, word in enumerate(suggestions, 1):
            print(f"{i}. {word}")
        
        choice = input("\nSelect a suggestion (number) or press Enter to skip: ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                selected_word = suggestions[idx]
                print(f"You selected: {selected_word}")
                trie.update_frequency(selected_word)
            else:
                print("Invalid selection.")
        
        print("-" * 40)


if __name__ == "__main__":
    run_autocomplete()