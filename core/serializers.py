from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserLoginInfo , User, updates

# Automatically fetches your project's active User model (Custom or Default)
User = get_user_model()

class UserLoginInfoSerializer(serializers.ModelSerializer):
    # Allows React to send an integer (ID) for the user field
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserLoginInfo
        fields = [
            'id', 
            'user', 
            'ip_address', 
            'city', 
            'region', 
            'country', 
            'browser', 
            'os', 
            'device', 
            'created_at'  # Included assuming you have a timestamp field
        ]
        # 'id' and 'created_at' should be read-only so React doesn't have to provide them
        read_only_fields = ['id', 'created_at']

    def validate_ip_address(self, value):
        """
        Optional: Basic sanitation field validation. 
        Ensures that if React sends an empty IP string, it defaults nicely.
        """
        if not value or value.strip() == "":
            return "0.0.0.0"
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()