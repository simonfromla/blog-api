from django import forms
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
    )

# Started off thinking about/defining the basic views needed
# Identify the need for a form in this app
# Created the UserLoginForm in forms.py
# Import the form into the views--(from here, can go straight to importing/adding the view into the urls)
# Updated the login_view with basic validation, and configured its "render"
# Created a basic template, form.html, corresponding to the render function
# Import the views into blog/urls.py and create the corresponding urls


User = get_user_model()
#not a ModelForm. Standard form. Will do checks inside the form..
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#run a clean method. Every form once doing validation, (See: login_view is.valid)
# will run a clean method which allows us to prevent certain things from happening, if they do happen.
# Method runs after is_valid returns True.
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

    #Another way to auth. Removes necessity for using authenticate method^.
    # Can customize filter according to email, etc.
    # If not using authenticate method^, then must definitely have check_password
    # method below.
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:

        #check if user exists. not logging the user in.
            user = authenticate(username=username, password=password)

            #If above^ does not give us a User model,
            if not user:
                raise forms.ValidationError("This user does not exist")
            #check if pw is correct. (in addition to above^ check, pw=pw)
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
            #If pass all validation checks, return the default data. Itself
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):

    #In order to add custom field(second email conf. field), add the fields here
    #Also add a field here, to override its corresponding field in the Meta class,
    # and to make it *required* in the form or add widget. (email and password)
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    #the pw widget makes it hidden
    password = forms.CharField(widget=forms.PasswordInput)

    # Meta class in form or admin: has to do with something that is not a field
    # STATE the fields we want to use from the model, and not create new fields
    # The order of fields listed here will reflect in the actual rendering
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]


#Same function as below, but overrides the clean method itself.
#Validation runs and gives a NON-field error, while the below clean_email2
# gives a[n] (on-the-)field error.
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     if email != email2:
    #         raise forms.ValidationError("Emails must match")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("This email has already been registered")

    #     return super(UserRegisterForm,self).clean(*args, **kwargs)



    #A clean function to make sure the emails match
    #See Documentation: Form and field validation
    # field called in clean_ and order of above Meta fields matters in determining
    # whether or not clean methods will come through.
    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        #Check that the emails match
        if email != email2:
            raise forms.ValidationError("Emails must match")

        #another validation to check if email already exists in the DB
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email

#These validations are not validations *on the model*, rather validations on the form.
#Ideally, would make custom User models with email being unique