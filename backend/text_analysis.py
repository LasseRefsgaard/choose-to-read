def lix_calculator(text):
    """Calculate the LIX readability score for given text.

    Returns the sum of average sentence length and percentage of long words (>6 chars).
    """
    total_words = 0
    long_words = 0

    sentences = text.split(".")
    # print(sentences)
    try:
        sentences.remove(" \n")
    except ValueError:
        pass

    sentence_lengths = []
    for sentence in sentences:
        words = sentence.split(" ")

        try:
            words.remove("")
        except ValueError:
            pass

        for word in words:
            total_words = total_words + 1
            if len(word) > 6:
                long_words = long_words + 1

        sentence_lengths.append(len(words))

    return round(sum(sentence_lengths) / len(sentence_lengths), 0) + round(
        long_words / (total_words / 100), 0
    )
