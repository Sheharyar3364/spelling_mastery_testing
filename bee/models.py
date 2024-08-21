from django.db import models
from django.core.exceptions import ValidationError
from nltk.corpus import brown, gutenberg, cmudict
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField  # Import for PostgreSQL, or use models.JSONField for Django 3.1+
from django.conf import settings  # Make sure to import settings


class Puzzle(models.Model):
    characters = models.CharField(max_length=6, unique=True, db_index=True)
    central_letter = models.CharField(max_length=1, db_index=True)

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
            set(gutenberg.words()) 
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

        # Save new valid words as answers in JSON format
        Answer.objects.update_or_create(
            puzzle=self, 
            defaults={'words': valid_words}
        )

    def get_valid_words(self):
        combined_words = (
            set(brown.words()) |
            set(gutenberg.words()) 
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



class Answer(models.Model):
    puzzle = models.OneToOneField(Puzzle, related_name='answers', on_delete=models.CASCADE)
    words = models.JSONField()  # Store answers in JSON format

    def __str__(self):
        return f"Answers for Puzzle {self.puzzle_id}"



@receiver(pre_save, sender=Puzzle)
def delete_previous_answers(sender, instance, **kwargs):
    if instance.pk:
        Answer.objects.filter(puzzle=instance).delete()



class UserGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, db_index=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    play_time = models.DurationField(null=True, blank=True)  # Store playtime as a duration
    status = models.IntegerField(default=0, db_index=True)
    foundWords = models.JSONField(default=list)

    # def calculate_play_time(self):
    #         self.play_time = self.end_time - self.start_time
    #         self.save()  # Save the calculated play time

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class PuzzleSolution(models.Model):
    user_game = models.ForeignKey(UserGame, on_delete=models.CASCADE, related_name='puzzle_solution', db_index=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, db_index=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.answer.word} by {self.user_game.user.username} in Puzzle {self.user_game.puzzle.id}"