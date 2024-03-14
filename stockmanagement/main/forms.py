from django import forms
from django.contrib.auth.forms import UserCreationForm
from.models import Product,Category,Branch,Type,Sale,Storeitem
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    

    class Meta:
        model = User
        fields =  ( 'username','password')


class ProductAddForm(forms.ModelForm):   
    class Meta:
        model = Product
        fields = ['part_number','part_name','price','product_category','car_type','reorder_level','is_used','qyt']



class CatAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class RertunForm(forms.ModelForm):
    quantity = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    class Meta:
        model = Storeitem
        fields = ['quantity']


class DistAddForm(UserCreationForm):
    class Meta:
        model = Branch
        fields = ['username','name']



class TypeAddForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'


class IssueForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['issue_quantity','issued_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['receive_quantity']


class SaleForm(forms.ModelForm):
     class Meta:
        model = Sale
        fields =  ['qty']

class SaleSearch(forms.ModelForm):
     start_date = forms.DateTimeField(required=False)
     end_date = forms.DateTimeField(required=False)
     print_pdf = forms.BooleanField(required=False)
     
     class Meta:
        model = Sale
        fields =  ['start_date','end_date']



