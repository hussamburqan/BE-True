from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrTelTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    تسجيل الدخول عبر:
      - email
      - tel_number
      - identifier (إيميل أو رقم هاتف)
    مع password طبعًا.
    """
    email = serializers.EmailField(required=False, allow_blank=True)
    tel_number = serializers.CharField(required=False, allow_blank=True)
    identifier = serializers.CharField(required=False, allow_blank=True)

    username_field = User.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name']         = getattr(user, 'name', '')
        token['email']        = getattr(user, 'email', '')
        token['tel_number']   = getattr(user, 'tel_number', '')
        token['is_staff']     = bool(getattr(user, 'is_staff', False))
        token['is_superuser'] = bool(getattr(user, 'is_superuser', False))
        return token

    def validate(self, attrs):

        email = attrs.pop('email', None)
        tel   = attrs.pop('tel_number', None)
        ident = attrs.pop('identifier', None)

        if not attrs.get(self.username_field):
            if email:
                attrs[self.username_field] = email.strip().lower()
            elif tel:
                try:
                    u = User.objects.get(tel_number=tel)
                    attrs[self.username_field] = getattr(u, self.username_field)
                except User.DoesNotExist:
                    pass
            elif ident:
                ident = ident.strip()
                if '@' in ident:
                    attrs[self.username_field] = ident.lower()
                else:
                    try:
                        u = User.objects.get(tel_number=ident)
                        attrs[self.username_field] = getattr(u, self.username_field)
                    except User.DoesNotExist:
                        pass

        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])

    class Meta:
        model = User
        fields = ['tel_number', 'name', 'email', 'password']

    def validate_email(self, value):
        return (value or '').strip().lower()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=False, allow_blank=True)
    tel_number = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "tel_number",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = ["id", "is_staff", "is_superuser"]

    def validate_email(self, value):
        value = (value or "").strip().lower()
        if not value:
            return value
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_tel_number(self, value):
        value = (value or "").strip()
        if not value:
            return value
        qs = User.objects.filter(tel_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def update(self, instance, validated_data):

        name = validated_data.get("name", None)
        email = validated_data.get("email", None)
        tel  = validated_data.get("tel_number", None)

        if name is not None:
            instance.name = name

        if email is not None:
            instance.email = (email or "").strip().lower()

        if tel is not None:
            instance.tel_number = (tel or "").strip()

        validated_data.pop("is_staff", None)
        validated_data.pop("is_superuser", None)

        instance.save()
        return instance