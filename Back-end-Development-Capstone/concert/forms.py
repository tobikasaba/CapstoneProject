from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


# Define a custom login form based on Django's authentication form.
class LoginForm(AuthenticationForm):
    # Create the username input field shown on the login form.
    username = forms.CharField(
        # Limit the username input to 100 characters.
        max_length=100,
        # Require the user to enter a username before submitting the form.
        required=True,
        # Render this field as a text input with HTML attributes for styling and UX.
        widget=forms.TextInput(
            # Provide HTML attributes for the rendered input element.
            attrs={
                # Show a hint inside the input box before the user types.
                "placeholder": "Username",
                # Apply the Bootstrap form-control CSS class.
                "class": "form-control",
            }
        ),
    )
    # Create the password input field shown on the login form.
    password = forms.CharField(
        # Limit the password input to 50 characters at the form level.
        max_length=50,
        # Require the user to enter a password before submitting the form.
        required=True,
        # Render this field as a password input so characters are hidden.
        widget=forms.PasswordInput(
            # Provide HTML attributes for the rendered password field.
            attrs={
                # Show a hint inside the password box.
                "placeholder": "Password",
                # Apply the Bootstrap form-control CSS class.
                "class": "form-control",
                # Provide a custom attribute often used by password toggle scripts.
                "data-toggle": "password",
                # Set the HTML id attribute for this input element.
                "id": "password",
                # Set the HTML name attribute for this input element.
                "name": "password",
            }
        ),
    )

    # Define metadata that tells Django which model and fields this form relates to.
    class Meta:
        # Associate this form with Django's built-in User model.
        model = User
        # Expose only the username and password fields in this form.
        fields = ["username", "password"]


# Define a custom sign-up form based on Django's authentication form.
class SignUpForm(AuthenticationForm):
    # Create the username input field shown on the sign-up form.
    username = forms.CharField(
        # Limit the username input to 100 characters.
        max_length=100,
        # Require the user to enter a username before submitting the form.
        required=True,
        # Render this field as a text input with HTML attributes for styling and UX.
        widget=forms.TextInput(
            # Provide HTML attributes for the rendered input element.
            attrs={
                # Show a hint inside the input box before the user types.
                "placeholder": "Username",
                # Apply the Bootstrap form-control CSS class.
                "class": "form-control",
            }
        ),
    )
    # Create the password input field shown on the sign-up form.
    password = forms.CharField(
        # Limit the password input to 50 characters at the form level.
        max_length=50,
        # Require the user to enter a password before submitting the form.
        required=True,
        # Render this field as a password input so characters are hidden.
        widget=forms.PasswordInput(
            # Provide HTML attributes for the rendered password field.
            attrs={
                # Show a hint inside the password box.
                "placeholder": "Password",
                # Apply the Bootstrap form-control CSS class.
                "class": "form-control",
                # Provide a custom attribute often used by password toggle scripts.
                "data-toggle": "password",
                # Set the HTML id attribute for this input element.
                "id": "password",
                # Set the HTML name attribute for this input element.
                "name": "password",
                # Add a minimum length hint for client-side browser validation.
                "minlength": "3"
            }
        ),
    )

    # Define metadata that tells Django which model and fields this form relates to.
    class Meta:
        # Associate this form with Django's built-in User model.
        model = User
        # Expose only the username and password fields in this form.
        fields = ["username", "password"]
