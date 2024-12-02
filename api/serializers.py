from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User, Task

#registerSerializer
class UserSerialzier(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
#loginSerializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # if not User.objects.filter(username = data['username']).exists():
        #     raise serializers.ValidationError('Username does not exists')
        # return data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')
        
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        return data
    

    def get_jwt_token(self, data):
        
        # user = authenticate(username = data['username'], password = data['password'])
        user = User.objects.get(username=data['username'])

        if not user:
            return({'message':'Invalid credentials'})
        refresh = RefreshToken.for_user(user)
        return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
                'id': user.id,
                'username': user.username
            }   
        }


#taskSerializer
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['date_created', 'date_completed', 'user']

    def validate(self, validated_data):
        if Task.objects.filter(title = validated_data['title']).exists():
            raise serializers.ValidationError('Title already exists')
        return validated_data