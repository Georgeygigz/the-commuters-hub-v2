from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework import generics,mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..helpers.renderers import RequestJSONRenderer
from .serializers import (RegistrationSerializer, LoginSerializer,
                          UserRetriveUpdateSerializer,UserSearchSerializer,
                        PasswordResetEmailSerializer)
from .tasks import send_mail_
from ..helpers.token import get_token_data, generate_password_reset_token
from .models import User
from ..helpers.pagination_helper import Pagination
from ..helpers.constants import (
    SIGNUP_SUCCESS_MESSAGE, VERIFICATION_SUCCESS_MSG,PASS_RESET_MESSAGE)


class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        data = serializer.data
        user_email = data['email']
        first_name = data['first_name']

        domain = settings.VERIFY_URL

        url = domain + str(data['token'])

        body = render_to_string('verify.html', {
            'link': url,
            'first_name': first_name
        })
        subject = 'Verify your email'
        message = 'Please verify your account.'
        # send email to the user for verification
        send_mail_.delay(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user_email],
            html_message=body,
            fail_silently=False,)

        return_message = {'message': SIGNUP_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)


class VerifyAPIView(generics.RetrieveAPIView):
    """
    A class to verify user using the token sent to the email
    """
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = UserRetriveUpdateSerializer
    @classmethod
    def get(self, request, token):
        """
        Overide the default get method
        """
        user = get_token_data(token)
        user.is_active = True
        user.save()
        return Response(data={"message": VERIFICATION_SUCCESS_MSG},
                        status=status.HTTP_200_OK)


class LoginAPIView(generics.CreateAPIView):
    # Login user class
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Class that handles retrieving and updating user info
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = UserRetriveUpdateSerializer

    def get(self, request, *args, **kwargs):
        """
        retrieve user details from the token provided
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        overide the default patch() method to enable
        the user update their details
        """
        data = request.data

        serializer = self.serializer_class(
            request.user, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersRetrieveSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve: Return users.
    list: Return a list of users
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(
        deleted=False, is_active=True).order_by('first_name')
    serializer_class = UserSearchSerializer
    pagination_class = Pagination
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name', 'surname',
                     'email', 'username', 'phone_number',)

    @action(methods=['GET'], detail=False, url_name='Search users')
    def search(self, request, *args, **kwargs):
        """
        Search users
        """
        return super().list(request, *args, **kwargs)


class PassResetEmailAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = PasswordResetEmailSerializer

    def post(self, request):
        """
        here, the user provides email to be used to get a link. The email must be registered,
        token gets generated and sent to users via link.
        """
        email = request.data.get('email', {})
        serializer = self.serializer_class(data={'email': email})
        serializer.is_valid(raise_exception=True)
        user = serializer.verify(email)
        message = "Please reset your password"
        subject = "Password reset"
        reset_link = settings.PASS_RESET_URL
        token = generate_password_reset_token(user.email, user.id)
        body = render_to_string('password_reset.html', {
            'link': reset_link + token,
            'name': user.first_name,
        })

        send_mail_.delay(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user.email],
            html_message=body,
            fail_silently=False,)
        return Response({"message": PASS_RESET_MESSAGE}, status=status.HTTP_200_OK)