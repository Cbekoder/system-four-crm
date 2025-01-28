from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role:
            data['role'] = self.user.role
        else:
            raise ValidationError({"error": "User role/ shouldn't be None"})
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'section']


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'role', 'section', 'date_joined'
        ]
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def validate(self, data):
        if not self.instance and 'password' not in data:
            raise serializers.ValidationError({'password': 'This field is required for new users.'})
        return data

    def create(self, validated_data):
        validated_data.pop('status', None)
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        salary_or_kpi = validated_data.pop('salary_or_kpi', None)
        role = validated_data.get('role', instance.role)

        if salary_or_kpi is not None:
            if role == 'doctor':
                instance.kpi = salary_or_kpi
            else:
                instance.salary = salary_or_kpi

        for attr, value in validated_data.items():
            if attr == 'password' and value:
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        #
        # if 'password' in validated_data:
        #     instance.password = make_password(validated_data['password'])

        instance.save()
        return instance

    def to_representation(self, instance):
        return UserDetailSerializer(instance).data
