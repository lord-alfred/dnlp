from dnlp.languages import FASTTEXT_LANGUAGES, FASTTEXT_LANGUAGES_EXTRA_DATA


def remap_prediction(prediction):
    result = []
    if not prediction[0]:
        return result

    for index in range(len(prediction[0])):
        lang = prediction[0][index].replace('__label__', '')

        result.append({
            'confidence': prediction[1][index],
            'code': lang,
            'name': FASTTEXT_LANGUAGES[lang],
            'family': FASTTEXT_LANGUAGES_EXTRA_DATA[lang][0],
            'endonym': FASTTEXT_LANGUAGES_EXTRA_DATA[lang][2],
            'iso639-1': FASTTEXT_LANGUAGES_EXTRA_DATA[lang][3],
            'iso639-2/T': FASTTEXT_LANGUAGES_EXTRA_DATA[lang][4],
            'iso639-2/B': FASTTEXT_LANGUAGES_EXTRA_DATA[lang][5],
            'iso639-3': FASTTEXT_LANGUAGES_EXTRA_DATA[lang][6],
        })

    return sorted(result, key=lambda d: d['confidence'], reverse=True)
