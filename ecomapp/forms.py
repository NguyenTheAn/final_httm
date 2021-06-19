from django import forms
from django.forms import fields
from .models import *
from django.contrib.auth.models import User
import datetime

METHOD =(
    ("1", "Cash"),
    ("2", "Banking"),
    ("3", "QRCode")
)

class CheckoutForm(forms.ModelForm):
    paymentMethod = forms.CharField(label = "Payment Method", widget=forms.Select(choices=METHOD))
    class Meta:
        model = Order
        fields = ["addressid", "voucherid",
                  "paymentMethod"]

class FeedBackForm(forms.ModelForm):
    content = forms.CharField(label = "Nội Dung", widget=forms.Textarea(attrs={'rows':2, 'cols':70}))
    rating = forms.TypedChoiceField(choices=[(x, x) for x in range(1, 6)], coerce=int, help_text = 'Units: ')
    class Meta:
        model = Feedback
        fields = ["content", "rating"]

class ReviewForm(forms.ModelForm):
    content = forms.CharField(label = "Nội Dung", widget=forms.Textarea(attrs={'rows':6, 'cols':100}))
    class Meta:
        model = Customerreview
        fields = ["content"]

class ReplyReviewForm(forms.ModelForm):
    content = forms.CharField(label = "Nội Dung", widget=forms.Textarea(attrs={'rows':6, 'cols':100}))
    class Meta:
        model = Reviewreply
        fields = ["content"]

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    phonenumber = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    full_name = forms.CharField(widget=forms.TextInput())
    city = forms.CharField(widget=forms.TextInput())
    district = forms.CharField(widget=forms.TextInput())
    town = forms.CharField(widget=forms.TextInput())
    street = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Customer
        fields = ["username", "phonenumber", "email", "full_name", "city", "district","town", "street", "description"]

class ShippingAddressCreateForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput())
    district = forms.CharField(widget=forms.TextInput())
    town = forms.CharField(widget=forms.TextInput())
    street = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = CustomerShippingaddress
        fields = ["city", "district","town", "street", "description"]

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    phonenumber = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    full_name = forms.CharField(widget=forms.TextInput())
    city = forms.CharField(widget=forms.TextInput())
    district = forms.CharField(widget=forms.TextInput())
    town = forms.CharField(widget=forms.TextInput())
    street = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Customer
        fields = ["username", "password", "phonenumber", "email", "full_name", "city", "district","town", "street", "description"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")

        return uname

TYPE =(
    ("1", "Clothes"),
    ("2", "Electronic"),
    ("3", "Book")
)

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    manufacturingdate = forms.DateField(initial=datetime.date.today)
    expirydate = forms.DateField(initial=datetime.date.today)
    name = forms.CharField(label = "Product Name")
    type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    slug = forms.SlugField()
    # price = forms.IntegerField(required=False)
    description = forms.CharField()
    images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Item
        fields = ["producer", "manufacturingdate", "expirydate", "name", "type", "slug", "price", "description", "images"]

class EditProductForm(forms.ModelForm):
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(), empty_label="-"*20)
    name = forms.CharField(label = "Product Name")
    type = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    manufacturingdate = forms.DateField(initial=datetime.date.today)
    expirydate = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Product
        fields = ["producer", "name", "type", "manufacturingdate", "expirydate"]

class EditItemForm(forms.ModelForm):
    price = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':50}))
    class Meta:
        model = Item
        fields= ["price", "description"]

class ImportProductForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(queryset= Supplier.objects.all())
    prodtype = forms.CharField(label = "Product Type", widget=forms.Select(choices=TYPE))
    product = forms.ModelChoiceField(queryset= Product.objects.all())
    number = forms.IntegerField()
    price = forms.IntegerField()

    class Meta:
        model = Importingrecord
        fields = ["supplier", "prodtype", "product", "number", "price"]

class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter the email used in customer account..."
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if Customer.objects.filter(userid__accountid__user__email=e).exists():
            pass
        else:
            raise forms.ValidationError(
                "Customer with this account does not exists..")
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password
