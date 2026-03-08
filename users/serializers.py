from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['role'] = user.role
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Añadirlos a la respuesta JSON inicial
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'id': self.user.id
        }

        return data
