import json

def tokenize(json_obj) -> dict[str, int]:
    curr = []
    tokens = []
    frequencies = {}
    for key, value in json_obj:
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
    return frequencies

def generate_report(frequencies: dict[str, int]):
    with open("url_responses.json", 'r') as json_file:
        data = json.load(json_file)
        tokenized = tokenize(data)

if __name__ == '__main__':
    generate_report()
