from Legobot.Lego import Lego
import logging
import os
import random
import yaml

logger = logging.getLogger(__name__)


class FactSphere(Lego):
    def __init__(self, baseplate, lock, *args, **kwargs):
        super().__init__(baseplate, lock)
        self.categories = self._get_categories()

    def listening_for(self, message):
        if message.get('text'):
            try:
                if message.get('text').startswith('!fact'):
                    return True
            except Exception as e:
                logger.error(('FactSphere lego failed to check the message'
                             ' text: {}'.format(e)))
                return False

    def handle(self, message):
        opts = self.set_opts(message)
        category = None
        if len(message['text'].split(' ')) > 1:
            category = message['text'].split(' ')[1]
        fact = self._get_random_fact(category=category)
        if fact is not None:
            response = self._format_response(fact)
            self.reply(message, response, opts)
        else:
            logger.error('There was an issue handling the message.')

    def _get_categories(self):
        facts = self._load_fact_data()
        if not facts:
            return None
        categories = list(set([fact['category'] for fact in facts['facts']]))
        return categories

    def _get_random_fact(self, category=None):
        facts = self._load_fact_data()
        if facts:
            facts = facts['facts']
        else:
            return None

        if category:
            if category in self.categories:
                facts = [fact for fact in facts
                         if fact['category'] == category]
        if facts is not None:
            fact = random.choice(facts)  # nosec
            return fact
        else:
            return None

    def _format_response(self, fact):
        response = '> {}\n-The Fact Sphere\n({})'.format(fact['fact'],
                                                         fact['audio'])
        return response

    def _load_fact_data(self):
        path = os.path.dirname(__file__)
        fact_file = path + '/facts.yaml'
        try:
            with open(fact_file, 'r') as f:
                facts = yaml.safe_load(f)
            return facts
        except Exception as e:
            logger.error('Error loading facts file: {}'.format(e))
            return None

    def set_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
            return opts
        except Exception as e:
            logger.error(('Could not identify message source in '
                         'message. Error: {}'.format(e)))

    def get_name(self):
        return 'fact_sphere'

    def get_help(self):
        return ('Return a random Fact Sphere fact. Usage: !fact '
                '[category_name].\nValid categories: {}').format(
                    ', '.join(self.categories)
                )
