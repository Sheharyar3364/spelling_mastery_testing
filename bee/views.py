from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Puzzle, Answer, UserGame
from .serializers import PuzzleSerializer, AnswerSerializer
import nltk
from nltk.corpus import brown, gutenberg, reuters, webtext, inaugural, state_union, cmudict
from rest_framework.decorators import action
from django.utils import timezone
from django.db import transaction




class PuzzleView(viewsets.ModelViewSet):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=['get'], url_path='unplayed_puzzle')
    def unplayed(self, request):
        user = request.user

        # Bulk create UserGame instances for puzzles that don't have a UserGame record for this user
        puzzles_without_usergame = Puzzle.objects.exclude(
            id__in=UserGame.objects.filter(user=user).values_list('puzzle_id', flat=True)
        )

        usergames_to_create = [
            UserGame(user=user, puzzle=puzzle, status=0) for puzzle in puzzles_without_usergame
        ]

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            UserGame.objects.bulk_create(usergames_to_create)

        # Filter UserGames for unplayed puzzles (status=0)
        unplayed_usergames = UserGame.objects.filter(user=user, status=0)

        if unplayed_usergames.exists():
            # Get the first unplayed puzzle
            first_unplayed_usergame = unplayed_usergames.first()
            puzzle = first_unplayed_usergame.puzzle

            # Serialize and return the puzzle data
            serializer = self.get_serializer(puzzle)

            # Include the id of the first_unplayed_usergame in the response data
            response_data = serializer.data
            response_data['user_game_id'] = first_unplayed_usergame.id

            return Response(response_data)
        else:
            return Response({'message': 'No unplayed puzzles available'}, status=404)



class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    @action(detail=False, methods=['get'], url_path='by-puzzle/<puzzle_id>')
    def by_puzzle(self, request, puzzle_id=None):
        answers = self.get_queryset().filter(puzzle_id=puzzle_id)
        serializer = self.get_serializer(answers, many=True)
        return Response(serializer.data)


    def list(self, request):
        # Fetch all Puzzle instances
        puzzles = Puzzle.objects.all()

        # Initialize a list to store all answers
        all_answers = []

        # Iterate over each Puzzle instance
        for puzzle in puzzles:
            # Check if answers already exist for this puzzle
            existing_answers = Answer.objects.filter(puzzle=puzzle)
            if existing_answers.exists():
                # If answers exist, add them to the list of all answers
                all_answers.extend(existing_answers)
            else:
                characters = puzzle.characters + puzzle.central_letter
                central_letter = puzzle.central_letter

                # Access words from NLTK corpora
                brown_words = set(brown.words())
                gutenberg_words = set(gutenberg.words())
                # reuters_words = set(reuters.words())
                # webtext_words = set(webtext.words())
                # inaugural_words = set(inaugural.words())
                # state_union_words = set(state_union.words())

                # Combine words into a single set to remove duplicates efficiently
                combined_words = (
                    brown_words |
                    gutenberg_words 
                )

                # Define the criteria for filtering words
                def is_valid_word(word):
                    word_set = set(word)
                    return (central_letter in word_set and 
                            set(word).issubset(set(characters)) and 
                            len(word) >= 4 and 
                            word.isalpha() and 
                            word.islower())

                # Filter and remove duplicates
                filtered_valid_words = {word.lower() for word in combined_words if is_valid_word(word.lower())}

                # Validate each word against the cmudict corpus
                cmudict_words = set(cmudict.words())

                # Save valid words to Answer model if not already saved
                for word in filtered_valid_words:
                    if word in cmudict_words:
                        answer_obj, created = Answer.objects.get_or_create(word=word, puzzle=puzzle)
                        if created:
                            all_answers.append(answer_obj)

        # Serialize all answers
        serializer = AnswerSerializer(all_answers, many=True)
        return Response(serializer.data)



class UserGameView(viewsets.ModelViewSet):
    queryset = UserGame.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='start_game')
    def start_game(self, request):
        puzzle_id = request.data.get('puzzle_id')
        puzzle = Puzzle.objects.get(pk=puzzle_id)

        user_game = UserGame.objects.create (
            user = request.user,
            puzzle = puzzle,
            start_time = timezone.now()
        )

        return Response({"user_game_id": user_game.id}, status=201)
    

    @action(detail=False, methods=['post'], url_path='complete_puzzle')  
    def complete_puzzle(self, request):
        user_game_id = request.data.get("gameid")
        user_game = UserGame.objects.get(pk=user_game_id)
        user_game.end_time = timezone.now()
        # user_game.calculate_play_time()
        user_game.status = 1
        user_game.save()

        return Response({"detail": "Puzzle completed successfully."}, status=200)
    
    
    @action(detail=False, methods=['post'], url_path='skip_puzzle')  
    def skip_puzzle(self, request):
        user_game_id = request.data.get("gameid")
        game_status = request.data.get("status")

        # Update the status directly without fetching the object
        UserGame.objects.filter(pk=user_game_id).update(status=game_status)

        return Response({"detail": "Puzzle skipped successfully."}, status=200)
