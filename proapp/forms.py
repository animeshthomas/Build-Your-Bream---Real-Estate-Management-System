from django import forms
from proapp.models import Ownerreg,Buyerreg,Property, Brqst,Purchase

class Ownerform(forms.ModelForm):
    class Meta:
        model = Ownerreg
        fields = ['oid', 'oname', 'phoneno', 'email', 'address', 'photo', 'username', 'password','rights']

class Buyerform(forms.ModelForm):
    class Meta:
        model = Buyerreg
        fields = ['bid','bname','phoneno','email','address','username','password',]
class Propertyform(forms.ModelForm):
    class Meta:
        model=Property
        fields = ['pid','oid','oname','ptype','ttype','otype','price','state','district','town','pincode','email','phoneno','builtarea','p1','p2','p3','p4','p5','des']
class Brequestform(forms.ModelForm):
    class Meta:
        model = Brqst
        fields = ['rqno','rqdate','bid','bname','pid','price','qprice']
class Purchaseform(forms.ModelForm):
    class Meta:
        model = Purchase
        fields= ['pno','pdate','pid','bid','bname','cardno','amtpaid']
