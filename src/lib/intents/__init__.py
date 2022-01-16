import nltk
# import re


class IntentAssistant:
    DEFAULT_INTENT = 'default_intent'
    DIFF_THRESHOLD = 0.4


    def __init__(self, intents, lang = 'en_EN'):
        self.intents = intents

        self.lang = lang


    def get_intent(self, text):
        for intent_name, examples in self.intents.items():
            for example in examples:
                diff = nltk.edit_distance(example, text)
                if (diff / len(text)) < self.DIFF_THRESHOLD:
                    return intent_name

        return self.DEFAULT_INTENT


    def is_intent_default(self, intent):
        return self.DEFAULT_INTENT == intent


# def clear(text):
#     return re.sub(r'[^_-a-zA-Z0-9]', "_", text)
#     return 1 if re.match('^[' + pattern + ']+$', str) is None else 0
