from trie import Trie

def load_words(trie):
    words = [
        "apple", "app", "apex",
        "bat", "ball", "batter",
        "cat", "call", "camel"
    ]

    for word in words:
        trie.insert(word)


def run_autocomplete():
    trie = Trie()
    load_words(trie)

    print("🔍 Smart Autocomplete System (type 'exit' to quit)\n")

    while True:
        prefix = input("Enter prefix: ").strip().lower()

        if prefix == "exit":
            print("Goodbye!")
            break

        suggestions = trie.search(prefix, top_k=5)

        if not suggestions:
            print("No suggestions found.\n")
            continue

        print("\nSuggestions:")
        for i, word in enumerate(suggestions, 1):
            print(f"{i}. {word}")

        # Simulate user clicking a suggestion
        choice = input("\nSelect a suggestion (number) or press Enter to skip: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                selected_word = suggestions[idx]
                print(f"You selected: {selected_word}")

                # 🔥 Boost frequency (learning)
                trie.update_frequency(selected_word)
            else:
                print("Invalid selection.")

        print("-" * 40)