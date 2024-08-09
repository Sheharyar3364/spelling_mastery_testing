from django.db import models
from django.core.exceptions import ValidationError
from nltk.corpus import brown, gutenberg, reuters, webtext, inaugural, state_union, cmudict
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Puzzle(models.Model):
    characters = models.CharField(max_length=6, unique=True)
    central_letter = models.CharField(max_length=1)

    def __str__(self):
        return self.characters

    def clean(self):
        if not self.is_valid_puzzle():
            raise ValidationError("No valid answer found for this puzzle. Please check the characters.")

    def save(self, *args, **kwargs):
        # Clean and validate the puzzle
        self.clean()
        super().save(*args, **kwargs)
        self.fetch_and_save_answers()

    def is_valid_puzzle(self):
        combined_words = (
            set(brown.words()) |
            set(gutenberg.words()) |
            set(reuters.words()) |
            set(webtext.words()) |
            set(inaugural.words()) |
            set(state_union.words())
        )

        def is_valid_word(word):
            word_set = set(word)
            return (
                self.central_letter in word_set and
                word_set.issubset(set(self.characters + self.central_letter)) and
                len(word) >= 4 and
                word.isalpha() and
                word.islower()
            )

        valid_words = {word.lower() for word in combined_words if is_valid_word(word.lower())}
        cmudict_words = set(cmudict.words())
        filtered_valid_words = [word for word in valid_words if word in cmudict_words]

        return bool(filtered_valid_words)

    def fetch_and_save_answers(self):
        valid_words = self.get_valid_words()
        if not valid_words:
            raise ValidationError("No valid answer found for this puzzle. The puzzle has been deleted.")

        # Clear existing answers
        self.answers.all().delete()

        # Save new valid words as answers
        Answer.objects.bulk_create([
            Answer(word=word, puzzle=self) for word in valid_words
        ])

    def get_valid_words(self):
        combined_words = (
            set(brown.words()) |
            set(gutenberg.words()) |
            set(reuters.words()) |
            set(webtext.words()) |
            set(inaugural.words()) |
            set(state_union.words())
        )

        def is_valid_word(word):
            word_set = set(word)
            return (
                self.central_letter in word_set and
                word_set.issubset(set(self.characters + self.central_letter)) and
                len(word) >= 4 and
                word.isalpha() and
                word.islower()
            )

        valid_words = {word.lower() for word in combined_words if is_valid_word(word.lower())}
        cmudict_words = set(cmudict.words())
        filtered_valid_words = [word for word in valid_words if word in cmudict_words]

        return filtered_valid_words


@receiver(pre_save, sender=Puzzle)
def delete_previous_answers(sender, instance, **kwargs):
    if instance.pk:
        previous_answers = Answer.objects.filter(puzzle=instance)
        previous_answers.delete()


class Answer(models.Model):
    word = models.CharField(max_length=100)
    puzzle = models.ForeignKey(Puzzle, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.word
