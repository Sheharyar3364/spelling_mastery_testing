from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from users.models import Note
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


from .serializers import NoteSerializer, UserRegistrationSerializer


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"msg": "Registration Succesful!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        token['level'] = user.level
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/refresh'
    ]

    return Response(routes)


class CustomDataView(APIView): 
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
            level_data = self.fetch_level_data(user)
            data = {
                "user_id": user_id,
                "level": level_data
            }

            return Response(data, status=status.HTTP_200_OK)
        except (InvalidToken, User.DoesNotExist):
            return Response({"error": "Invalid refresh token or user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    def fetch_level_data(self, user):
        # Fetch the level of the user
        return user.level
    
class UpdateLevelView(APIView):
    permission_classes = [IsAuthenticated]  # Class attribute

    def post(self, request, *args, **kwargs):
        user = request.user  # Get the currently authenticated user
        user.level += 1  # Increment the user's level or apply your business logic
        user.save()  # Save the user's updated level to the database
        return Response({"level": user.level}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = user.note_set.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

