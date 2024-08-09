# bee/management/commands/download_nltk_data.py

from django.core.management.base import BaseCommand
import nltk

class Command(BaseCommand):
    help = 'Download necessary NLTK corpora'

    def handle(self, *args, **kwargs):
        self.stdout.write('Downloading NLTK corpora...')
        nltk.download('brown')
        nltk.download('gutenberg')
        nltk.download('reuters')
        nltk.download('webtext')
        nltk.download('inaugural')
        nltk.download('state_union')
        nltk.download('cmudict')
        self.stdout.write('Download complete.')
