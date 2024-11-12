# destinations/forms.py
from django import forms
from .models import Booking, Category, Destination, DestinationImage, Review, User,Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location']


class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = ['name', 'description', 'location', 'price', 'categories']
    
    # Customizing the category field (optional)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class DestinationImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = DestinationImage
        fields = ['image']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['content', 'rating']

    # Optional: Custom validation for rating field
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'payment_method']  # Add payment_method to the fields list
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Optional: You could add labels or initial values here if needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].widget = forms.Select(choices=Booking.PAYMENT_METHOD_CHOICES)
        self.fields['payment_method'].label = "Payment Method"
