import random


class RandomWordGenerator:
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    @classmethod
    def generate_file(cls, filename: str, filepath: str, rows: int):
        with open(filepath + filename, 'w') as f:
            for row in range(rows):
                f.write(cls.__random_words() + '\n')

    @classmethod
    def generate_word_list(cls, rows: int) -> list:
        words = []
        for row in range(rows):
            words.append(cls.__random_words())

        return words

    @classmethod
    def generate_int_list(cls, rows: int, int_size: int) -> list:
        ints = set()
        for row in range(rows):
            ints.add(random.randint(0, int_size))

        return [i for i in ints]

    @classmethod
    def __random_words(cls, word_length=15, allow_upper=False) -> str:
        word = ''
        for i in range(word_length):
            index = random.randint(0, word_length + 1)
            word += cls.ALPHABET[index].upper() if allow_upper and random.randint(0, 2) == 1 else cls.ALPHABET[index]

        return word


if __name__ == '__main__':
    RandomWordGenerator.generate_file('temp1000rows', '/Users/jlonghurst/Dropbox/Projects/standard_library/', 1000)
