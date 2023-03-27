from allauth.account.forms import SignupForm
from django import forms
from .models import ExtendSignup, Profile
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
)


class MyCustomSignupForm(SignupForm):
    # Added extra "type" field to the signup form
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type')

    # Save the signup form data
    def save(self, request):
        """
        save : Method to save the signup form data
        :param request:
        :return user: object
        """
        # Ensure you call the parent classes save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        ExtendSignup.objects.get_or_create(type=request.POST['type'], user_id=user.id)
        # You must return the original result.
        return user


# UserForm  fields to edit profile of the user.
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


# ProfileForm fields to edit profile of the user.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'city', 'profile_picture')
