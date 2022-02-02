import sys, getopt
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
        logging.debug(f'BOT_CONFIG: loaded "{len(self.INTENTS.keys())}" intents')

        # intent examples
        self.INTENTS_EXAMPLES = {}
        for intent_name, intent_value in self.INTENTS.items():
            if len(intent_value[self.CONFIG_SECTION_INTENTS_EXAMPLES]) == 0:
                raise ValueError(f"Oops! Bad config. Not intent '{intent_name}' has no examples!")

            self.INTENTS_EXAMPLES[intent_name] = intent_value[self.CONFIG_SECTION_INTENTS_EXAMPLES]

        # failure_phrases
        self.PHRASES = config[self.CONFIG_SECTION_FAILURE_PHRASES]
        logging.debug(f'BOT_CONFIG: loaded "{len(self.PHRASES)}" failure_phrases')

        self.intentAssistant = intents.IntentAssistant(self.INTENTS_EXAMPLES)


    def answer(self, phrase):
        # NLU
        intent = self.intentAssistant.get_intent(phrase)
        if not self.intentAssistant.is_intent_default(intent):
            answer = self.gen_answer_by_intent(intent)
            if answer:
                return answer

        return self.gen_random_answer()


    def gen_answer_by_intent(self, intent):
        responses = self.INTENTS[intent]['responses']

        return random.choice(responses)


    def gen_random_answer(self):
        return random.choice(self.PHRASES)


#-----------------------------------#
# MAIN

def main(argv):
    BOT_STOP_WORD = '/stop'

    # arguments
    try:
        opts, args = getopt.getopt(argv, "-v")
    except getopt.GetoptError:
        raise getopt.GetoptError
        sys.exit(2)

    is_verbose_mode = False
    for opt, arg in opts:
        if opt == '-v':
            is_verbose_mode = True

    # logging
    logger = logging.getLogger(__name__)
    logging_verbosity = logging.DEBUG if is_verbose_mode else logging.WARNING
    logging.basicConfig(level=logging_verbosity, format='[%(asctime)s] %(levelname)s: %(message)s')

    # configs
    with open('data/bot_config.json') as f:
        BOT_CONFIG = json.load(f)
    bot = Bot(BOT_CONFIG)

    # non-interactive mode
    if len(args) == 1:
        input_text = args[0]
        print(f"- {input_text}")
        print(f"- {bot.answer(input_text)}")
        return

    # interactive mode
    input_text = ''
    while True:
        input_text = input()
        if input_text == BOT_STOP_WORD:
            break

        print(bot.answer(input_text))


#------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])
