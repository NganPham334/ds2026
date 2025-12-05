import string
from collections import defaultdict

def mapper(text):
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator).lower()
    for word in clean_text.split():
        yield (word, 1)

def reducer(key, values):
    return key, sum(values)

if __name__ == "__main__":
    input_text = """three swiss witch-bitches, which wished to be switched swiss witch-bitches, watch three swiss swatch watch switches.
which swiss witch-bitch, which wishes to be a switched witch-bitch, wishes to watch which swiss swatch watch switch?"""

    mapped_data = []
    for line in input_text.split('\n'):
        mapped_data.extend(mapper(line))

    shuffled_data = defaultdict(list)
    for key, value in mapped_data:
        shuffled_data[key].append(value)

    for key in sorted(shuffled_data.keys()):
        word, count = reducer(key, shuffled_data[key])
        print(f"{word}: {count}")