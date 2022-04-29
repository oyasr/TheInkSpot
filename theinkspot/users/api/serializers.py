from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

     


class RegisterUser(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=15, write_only=True)
    email = serializers.EmailField(max_length=225, min_length=8)
    name = serializers.CharField(max_length=155, min_length=8)
    username = serializers.CharField(max_length=155, min_length=8)
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']
    
    
    
    def validate(self, attrs):
        if not attrs.get('email'):
            raise serializers.ValidationErrot('User should have an email')
        if not attrs.get('name'):
            raise serializers.ValidationErrot('User should have a name')
        if not attrs.get('username'):
            raise serializers.ValidationErrot('User should have a username')
        if User.objects.filter(email=attrs['email']):
            raise serializers.ValidationErrot({'email':'Email already exists'})
        if User.objects.filter(email=attrs['username']):  
            raise serializers.ValidationErrot({'username':'username already exists'})

        return attrs

    def create(self, validation_data):
        return User.objects.create_user(**validation_data)  