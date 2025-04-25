import json

def tokenize(text: str, frequencies) -> dict[str, int]:
    curr = []
    tokens = []
    frequencies = {}
    for char in text:
        char_lower = char.lower()
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
    return frequencies

def generate_report(frequencies: dict[str, int]):
    with open("url_responses.json", 'r') as json_file:
        data = json.load(json_file)
        for item in data:
            tokenize(data[item])
