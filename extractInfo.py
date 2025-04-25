import json

def tokenize(json_obj) -> dict[str, int]:
    num_unique = 0
    longest = {
        "length": -1,
        "url": ""
    }
    curr = []
    tokens = []
    frequencies = {}
    for key, value in json_obj:
        if value != "":
            num_unique+=1
        char_lower = value.lower()
        if char_lower.isalnum():
            curr.append(char_lower)
        else:
            if curr:
                tokens.append(''.join(curr))
                curr = []
    if curr:
        tokens.append(''.join(curr))
    for token in tokens:

        frequencies[token] = frequencies.get(token, 0) + 1
    print("Unique Pages: " + num_unique)
    print(longest["url"] + ": " + str(longest["length"]))
    return frequencies

def print_frequencies(frequencies: dict[str, int]) -> None:
    sorted_items = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))
    for token, count in sorted_items[:50]:
        print(f"{token} - {count}")

def generate_report():
    with open("url_responses.json", 'r') as json_file:
        data = json.load(json_file)
        tokenized = tokenize(data)
        print_frequencies(tokenized)

if __name__ == '__main__':
    generate_report()
