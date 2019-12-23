from unittest.mock import patch, Mock
from .base_test import TestBaseCase
from ...authentication.tasks import send_mail_

class SendEmailTest(TestBaseCase):
    """
    Test send email
    """
    @patch('app.api.authentication.tasks.send_mail')
    def test_send_email_succeeds(self, mock_send_mail):
        """
        Test send email succeeds
        """
        mock_send_mail.side_effect = Mock(return_value=True)
        send_mail_(
            subject="subject",
            message="message",
            from_email="test-sender@email.com",
            recipient_list=["test@email.com"],
            html_message="body",
            fail_silently=False,)
        self.assertTrue(mock_send_mail.assert_called)

    def test_send_email_without_subject_fails(self):
        """
        Test send email without subject fails
        """
        send_mail_(
            message="message",
            from_email="test-sender@email.com",
            recipient_list=["test@email.com"],
            html_message="body",
            fail_silently=False,)
        self.assertRaises(Exception, """missing 1 required positional argument: 'subject'""")
