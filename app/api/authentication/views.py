from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..helpers.renderers import RequestJSONRenderer
from .serializers import RegistrationSerializer
from ..helpers.constants import SIGNUP_SUCCESS_MESSAGE
from .tasks import send_mail_


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
