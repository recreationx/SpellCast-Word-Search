import string

# Letter values
LETTERS_AND_VALUES = {
    "a": 1, "b": 4, "c": 5, "d": 3, "e": 1, "f": 5, "g": 3, "h": 4, "i": 1, "j": 7, "k": 3,
    "l": 3, "m": 4, "n": 2, "o": 1, "p": 4, "q": 8, "r": 2, "s": 2, "t": 2, "u": 4, "v": 5,
    "w": 5, "x": 7, "y": 4, "z": 8,
}

# Trie node for efficient prefix checking
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

# Build a trie from the given dictionary
def build_trie(dictionary):
    root = TrieNode()
    for word in dictionary:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    return root

# Check if the move is valid
def is_valid_move(x, y, visited):
    return 0 <= x < 5 and 0 <= y < 5 and not visited[x][y]

# Recursive function to find words with optional letter swapping
def find_words_with_swaps(x, y, grid, visited, current_word, trie_node, found_words, current_value, swaps_remaining):
    visited[x][y] = True
    current_char = grid[x][y]
    current_word += current_char
    current_value += LETTERS_AND_VALUES[current_char]

    if current_char in trie_node.children:
        trie_node = trie_node.children[current_char]
        if trie_node.is_end_of_word:
            found_words[current_word] = current_value

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(new_x, new_y, visited):
                find_words_with_swaps(new_x, new_y, grid, visited, current_word, trie_node, found_words, current_value, swaps_remaining)

    if swaps_remaining > 0:
        # Perform letter swapping
        original_char = grid[x][y]
        for swap_char in string.ascii_lowercase:
            if swap_char != original_char:
                # Swap the letter
                grid[x][y] = swap_char
                swapped_value = LETTERS_AND_VALUES[swap_char]

                # Adjust the current value and continue the search
                adjusted_current_value = current_value - LETTERS_AND_VALUES[original_char] + swapped_value
                find_words_with_swaps(x, y, grid, visited, current_word[:-1], trie_node, found_words, adjusted_current_value, swaps_remaining - 1)

        # Restore the original letter
        grid[x][y] = original_char

    visited[x][y] = False

# Function to find the highest value word with optional letter swapping
def highest_value_word_with_swaps(grid, dictionary, max_swaps):
    trie_root = build_trie(dictionary)
    found_words = {}
    visited = [[False for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            find_words_with_swaps(i, j, grid, visited, "", trie_root, found_words, 0, max_swaps)

    return max(found_words.items(), key=lambda item: item[1], default=("No valid word", 0))

# Load the dictionary from the file
sample_dictionary = set()
with open("words.txt", "r") as file:
    for line in file:
        word = line.strip().lower()
        if word:
            sample_dictionary.add(word)

grid_string = input("Enter a 25-character string for the grid: ").lower()

if len(grid_string) != 25:
    print("Invalid input length. Please enter exactly 25 characters.")
else:
    grid = [list(grid_string[i:i+5]) for i in range(0, 25, 5)]

    # Now grid is formatted as a 5x5 list of characters
    print("Formatted 5x5 grid:")
    for row in grid:
        print(row)

# Find the highest value word with no swap
highest_value_word_no_swap = highest_value_word_with_swaps(grid, sample_dictionary, 0)

# Find the highest value word with one-letter swap
highest_value_word_one_swap = highest_value_word_with_swaps(grid, sample_dictionary, 1)

# Find the highest value word with two-letter swaps
highest_value_word_two_swaps = highest_value_word_with_swaps(grid, sample_dictionary, 2)

print(highest_value_word_no_swap, highest_value_word_one_swap, highest_value_word_two_swaps)



