from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
class PasswordField(serializers.CharField):
    def get_value(self, dictionary):
        if 'password' in dictionary:
            return dictionary['password']
        return super().get_value(dictionary)

class UserSerializer(serializers.ModelSerializer):
    password = PasswordField(write_only=True, required=False, allow_blank=False, trim_whitespace=False)
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','matricula','password','is_active','is_staff']
        read_only_fields = ['id']
    def validate(self, attrs):
        if self.instance is None and 'password' not in attrs:
            raise serializers.ValidationError({'password':'Este campo es obligatorio al crear un usuario.'})
        if 'password' in attrs:
            candidate = User(**{k:v for k,v in attrs.items() if k != 'password'})
            try:
                validate_password(attrs['password'], candidate)
            except ValidationError as exc:
                raise serializers.ValidationError({'password':list(exc.messages)})
        return attrs
    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        # Si la peticion omite password, conserva exactamente el hash del usuario editado.
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','matricula','is_active','is_staff']
