from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

# have to change to remove django.utils.six package
class TokenGenerator(PasswordResetTokenGenerator):
    # account_activation_token = TokenGenerator()

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()