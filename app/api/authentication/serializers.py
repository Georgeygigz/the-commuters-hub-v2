from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from ..helpers.serialization_errors import error_dict
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure email is provided and is unique
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Email"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
        }
    )
    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        min_length=8,
        max_length=30,
        required=True,
        allow_null=False,
        write_only=True,
        error_messages={
            'required': error_dict['required'],
            'min_length': error_dict['min_length'].format("Password", "8"),
            'max_length': 'Password cannot be more than 30 characters',
            'invalid': error_dict['invalid_password'],
        }
    )
    # Ensure that the first_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed
    first_name = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('First name')
        }
    )

    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Username"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Username')
        }
    )

    # Ensure that the last_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed
    last_name = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Last name')
        }
    )
    # Ensure that the last_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed
    surname = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Surname')
        }
    )

    id_number = serializers.IntegerField(
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Id number"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_id_number']
        }
    )

    phone_number = serializers.RegexField(
        regex='^(?:\B\+ ?254|\b0)(?: *[(-]? *\d(?:[ \d]*\d)?)? *(?:[)-] *)?\d+ *(?:[/)-] *)?\d+ *(?:[/)-] *)?\d+(?: *- *\d+)?',
        allow_null=False,
        required=True,
        min_length=10,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Phone number"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
            'min_length': error_dict['min_length'].format("Phone number", "10"),
            'invalid': error_dict['invalid_phone_no']
        }
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['first_name', 'last_name', 'surname', 'email', 'username',
                  'password', 'id_number', 'phone_number', 'token', ]

    @classmethod
    def create(self, data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**data)


class LoginSerializer(serializers.Serializer):
    """Login serializer Class"""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    @staticmethod
    def validate(data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(email=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'token': user.token
        }

class UserRetriveUpdateSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    id = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    surname = serializers.CharField(read_only=True)
    phone_number = serializers.RegexField(
        regex='^(?:\B\+ ?254|\b0)(?: *[(-]? *\d(?:[ \d]*\d)?)? *(?:[)-] *)?\d+ *(?:[/)-] *)?\d+ *(?:[/)-] *)?\d+(?: *- *\d+)?',
        allow_null=False,
        required=False,
        min_length=10,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Phone number"),
            )
        ],
        error_messages={
            'min_length': error_dict['min_length'].format("Phone number", "10"),
            'invalid': error_dict['invalid_phone_no']
        }
    )
    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        min_length=8,
        max_length=30,
        required=False,
        write_only=True,
        allow_null=False,
        error_messages={
            'min_length': error_dict['min_length'].format("Password", "8"),
            'max_length': 'Password cannot be more than 30 characters',
            'invalid': error_dict['invalid_password'],
        }
    )
    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Username"),
            )
        ],
        error_messages={
            'invalid': error_dict['invalid_name'].format('Username')
        }
    )

    @classmethod
    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()
        return instance

    class Meta:
        model = User
        exclude = ('last_login', 'is_superuser', 'deleted', 'id_number',
                   'is_active', 'is_staff', 'groups', 'user_permissions')


class UserSearchSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User search objects."""
    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['first_name', 'last_name', 'surname', 'email', 'username',
                  'phone_number', 'id']


class PasswordResetEmailSerializer(serializers.Serializer):
    """
    serializes email
    """
    email = serializers.EmailField(max_length=255, required=True)

    @classmethod
    def verify(self, email):
        """
        Verify that the email exists in the database
        Args:
            self (instance): and instance of the class
            email (str): email to be verified
        Return:
            user (obj): the user object
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "The email provided is not registered"
            )
        # Check this user is activated
        if not user.is_active:
            raise serializers.ValidationError('This user is deactivated')
        return user
