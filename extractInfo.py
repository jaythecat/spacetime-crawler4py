import json
import re

STOP_WORDS = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
              "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
              "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
              "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
              "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
              "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
              "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
              "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
              "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
              "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
              "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
              "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
              "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
              "yours", "yourself", "yourselves"}


def tokenize(json_obj):
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
        filtered_words = [
            word for word in filtered_words
            # this is O(1) bc STOP_WORDS is a set ;)
            if word.isalnum() and word not in STOP_WORDS
        ]

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
        tokenize(data)


if __name__ == '__main__':
    generate_report()
