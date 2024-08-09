import os
from django.core.management.base import BaseCommand
from django.conf import settings
import nltk

class Command(BaseCommand):
    help = 'Download necessary NLTK corpora'

    def handle(self, *args, **kwargs):
        # Define the path to save NLTK data
        nltk_data_path = os.path.join(settings.BASE_DIR, 'nltk_data')

        # Ensure the directory exists
        os.makedirs(nltk_data_path, exist_ok=True)

        # Append the new path to NLTK's data path
        nltk.data.path.append(nltk_data_path)
        print(nltk.data.path)

        # Print the path for debugging
        self.stdout.write(f"NLTK data will be saved to: {nltk_data_path}")

        # Download the necessary corpora to the specified directory
        self.stdout.write('Downloading NLTK corpora...')
        nltk.download('brown', download_dir=nltk_data_path)
        nltk.download('gutenberg', download_dir=nltk_data_path)
        nltk.download('reuters', download_dir=nltk_data_path)
        nltk.download('webtext', download_dir=nltk_data_path)
        nltk.download('inaugural', download_dir=nltk_data_path)
        nltk.download('state_union', download_dir=nltk_data_path)
        nltk.download('cmudict', download_dir=nltk_data_path)
        self.stdout.write('Download complete.')

