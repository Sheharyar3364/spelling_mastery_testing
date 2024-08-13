from rest_framework import serializers
from .models import Puzzle, Answer


class PuzzleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puzzle
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    words = serializers.JSONField()  # Specify that words is a JSON field

    class Meta:
        model = Answer
        fields = '__all__'  # Include all fields, including 'words'