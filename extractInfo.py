import json
import re


def tokenize(json_obj) -> dict[str, int]:
    frequencies = {}
    filtered_words = ""
    unique_pages = 0
    longest = {
        "length": -1,
        "url": ""
    }
    for url, text in json_obj.items():
        unique_pages += 1
        if not text:
            continue
        words = text.lower().split()
        filtered_words = [re.sub(r'[^a-z0-9]', '', word) for word in words]
        filtered_words = [word for word in filtered_words if word.isalnum()]

        if len(filtered_words) > longest["length"]:
            longest["length"] = len(filtered_words)
            longest["url"] = url

    for token in filtered_words:
        frequencies[token] = frequencies.get(token, 0) + 1
    print(f"Unique Pages: {unique_pages}")
    print(longest["url"] + ": " + str(longest["length"]))
    print_frequencies(frequencies)


def print_frequencies(frequencies: dict[str, int]) -> None:
    sorted_items = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))
    i = 1
    for token, count in sorted_items[:50]:
        print(f"{i}. {token} - {count}")
        i += 1


def generate_report():
    with open("url_responses.json", 'r') as json_file:
        data = json.load(json_file)
        tokenized = tokenize(data)


if __name__ == '__main__':
    generate_report()
