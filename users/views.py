from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from users.serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "email": user.email,
                "message": "User create successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return Response(
                {"detail": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)

        response = Response({"detail": "Login successful"})

        response.set_cookie(
            key="access",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 10,
            path="/",
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,
            path="/",
        )
        
        return response
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def refresh(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return Response({"detail": "No refresh token"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            return Response({"detail": "Invalid refresh"},
                            status=status.HTTP_400_BAD_REQUEST)

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key="access",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 10,
            path="/",
        )

        return response
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def logout(self, request):
        response = Response({"detail": "Logged out"})
        response.delete_cookie("access", path="/")
        response.delete_cookie("refresh", path="/")
        return response

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)