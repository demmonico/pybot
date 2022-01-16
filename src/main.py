import random
import json
import logging
import lib.intents as intents


class Bot:
    CONFIG_SECTION_INTENTS = 'intents'
    CONFIG_SECTION_INTENTS_EXAMPLES = 'examples'
    CONFIG_SECTION_FAILURE_PHRASES = 'failure_phrases'


    def __init__(self, config):
        # intents
        self.INTENTS = config[self.CONFIG_SECTION_INTENTS]
        print(f'BOT_CONFIG: loaded "{len(self.INTENTS.keys())}" intents')

        # intent examples
        self.INTENTS_EXAMPLES = {}
        for intent_name, intent_value in self.INTENTS.items():
            if len(intent_value[self.CONFIG_SECTION_INTENTS_EXAMPLES]) == 0:
                raise ValueError(f"Oops! Bad config. Not intent '{intent_name}' has no examples!")

            self.INTENTS_EXAMPLES[intent_name] = intent_value[self.CONFIG_SECTION_INTENTS_EXAMPLES]

        # failure_phrases
        self.PHRASES = config[self.CONFIG_SECTION_FAILURE_PHRASES]
        print(f'BOT_CONFIG: loaded "{len(self.PHRASES)}" failure_phrases')

        self.intentAssistant = intents.IntentAssistant(self.INTENTS_EXAMPLES)

        print('-' * 20)


    def answer(self, phrase):
        # NLU
        intent = self.intentAssistant.get_intent(phrase)
        if not self.intentAssistant.is_intent_default(intent):
            answer = self.gen_answer_by_intent(intent)
            if answer:
                return answer

        return gen_random_answer()


    def gen_answer_by_intent(self, intent):
        responses = self.INTENTS[intent]['responses']

        return random.choice(responses)


    def gen_random_answer(self):
        return random.choice(BOT_CONFIG[self.CONFIG_SECTION_FAILURE_PHRASES])


#-----------------------------------#
# MAIN

def main():
# TODO
#     logger = logging.getLogger(__name__)
#     logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

    with open('data/bot_config.json') as f:
        BOT_CONFIG = json.load(f)
    bot = Bot(BOT_CONFIG)

    for phrase in ['Helllo', 'How are you?', 'Bye']:
        print(bot.answer(phrase))

#------------------------------#

if __name__ == '__main__':
    main()
