from django.contrib.auth import get_user_model
from rest_framework import serializers
from .helpers import check_password_strength
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
    password_confirmation = serializers.CharField(max_length=128, min_length=15, write_only=True)
    email = serializers.EmailField(max_length=225, min_length=8)
    name = serializers.CharField(max_length=155, min_length=8)
    username = serializers.CharField(max_length=155, min_length=8)
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password','password_confirmation']
    
    
    
    def validate(self, attrs):
        if not attrs.get('email'):
            raise serializers.ValidationError({'email_error','User should have a email'})

        if not attrs.get('name'):
            raise serializers.ValidationError({'name_error':'User should have a name'})
        
        if not attrs.get('username'):
            raise serializers.ValidationError({'username_error':'User should have a username'})
        
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError({'password_confirmation_error':'Password and confirmation should be identical'})
        
        if not check_password_strength(attrs.get('password')):
            raise serializers.ValidationError({'password_strength_error':
                'Password should be at least 15 characters and contain at least lowercase/uppercase character and numbers'})

        if User.objects.filter(email=attrs['email']):
            raise serializers.ValidationError({'email_duplication':'This email already exists'})
        
        if User.objects.filter(username=attrs['username']):  
            raise serializers.ValidationError({'username_duplication':'This username already exists'})

        return attrs

    def create(self, validation_data):
        return User.objects.create_user(validation_data['name'],
                                        validation_data['username'],
                                        validation_data['email'],
                                        validation_data['password'])  