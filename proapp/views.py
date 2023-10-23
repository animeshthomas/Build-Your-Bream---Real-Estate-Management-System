from django.shortcuts import render,redirect
from django.http import HttpResponse
from proapp.models import Ownerreg,Buyerreg,Property,Brqst,Purchase
from proapp.forms import Buyerform,Ownerform,Propertyform,Brequestform,Purchaseform
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.db.models.functions import Coalesce
from django.db.models import Max, Value
from datetime import date

class Addowner(CreateView):
    template_name = "add_owner.html"
    form_class = Ownerform
    success_url = "/"

def home(request):
    return render(request,"home.html")

class Listowner(ListView):
    template_name ="list_owner.html"
    model = Ownerreg
    context_object_name = "a"

class Addbuyer(CreateView):
    template_name = "add_buyer.html"
    form_class = Buyerform
    success_url = "/"


class Listbuyer(ListView):
    template_name = "list_buyer.html"
    model = Buyerreg
    context_object_name = "x"

class Bedit(UpdateView):
    template_name = "add_buyer.html"
    model = Buyerreg
    form_class = Buyerform
    context_object_name = "x"
    success_url = "/"
class Oedit(UpdateView):
    template_name = "add_owner.html"
    model = Ownerreg
    form_class = Ownerform
    context_object_name = "a"
    success_url = "/"
class Bdelete(DeleteView):
    template_name = "bdelete.html"
    model = Buyerreg
    form_class = Buyerform
    context_object_name = "x"
    success_url = "/"
class Odelete(DeleteView):
    template_name = "Odelete.html"
    model = Ownerreg
    form_class = Ownerform
    context_object_name = "a"
    success_url = "/"

def log(request):
    return render(request, "login.html")

def login(request):
    if  request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        obj= Ownerreg.objects.filter(username=username,password=password)
        obj1 = Buyerreg.objects.filter(username=username, password=password)
        if obj.filter(username=username,password=password).exists():
            for i in obj:
                y=i.oid
                x=i.rights
                z=i.oname
                request.session['oname']=z
                request.session['username']=username
                request.session['password']=password
                request.session['oid']=y
                request.session['rights']=x
                if x=='A':
                    return render(request, "admin_home.html")
                elif x=='N':
                    return render(request, "proces.html")
                elif x=="AP":
                    return render(request, "owner_home.html")
                elif x=='R':
                    return render(request, "rejected.html")
                else:
                    return render(request, "buyer_home.html")
        elif obj1.filter(username=username,password=password):
            for i in obj1:
                z = i.bid

            request.session['bid'] = z
            return render(request,"buyer_home.html")
        else:
            return render(request, "invalid.html")
    else:
        return render(request,"login.html")
def ownerapprove(request):
    orec=Ownerreg.objects.filter(rights='N')
    return render(request,'')
def ch(request):
    a = Ownerreg.objects.filter(rights='N')
    return render(request, "ownerrights.html",{"a":a})

def updaterights(request,oid):
    Ownerreg.objects.filter(oid=oid).update(rights='AP')
    return render(request,"admin_home.html")


def oreject(request,oid):
    Ownerreg.objects.filter(oid=oid).update(rights='R')
    return render(request, "admin_home.html")


def editowner(request):
    oid=Ownerreg.objects.get(pk=request.session['oid'])  #rec variable rcode is theid
    form=Ownerform(instance=oid)
    return render(request,'ownerupdate.html',{"form":form,"oid": oid})


def updateowner(request):
    oid=Ownerreg.objects.get(pk=request.session['oid'])
    form=Ownerform(request.POST,instance=oid)
    if form.is_valid():
        form.save()
        return render(request, 'owner_home.html',{"oid":oid})
    return render(request,'rejected.html',{"oid":oid})
def editbuyer(request):
    bid=Buyerreg.objects.get(pk=request.session['bid'])  #rec variable rcode is theid
    form=Buyerform(instance=bid)
    return render(request,'buyerupdate.html',{"form":form,"bid": bid})


def updatebuyer(request):
    rtos=Buyerreg.objects.get(pk=request.session['bid'])
    form=Buyerform(request.POST,instance=rtos)
    if form.is_valid():
        form.save()
        return render(request, 'buyer_home.html')
    return render(request,'rejected.html')

class Addproperty(CreateView):
    template_name = "add_property.html"
    form_class = Propertyform
    success_url = "/"

    def get_initial(self,*args,**kwargs):
        max_pid = Property.objects.aggregate(max_pid=Coalesce(Max('pid'),Value(0)))['max_pid']
        pid =int(max_pid)+ 1
        initial = super(Addproperty, self).get_initial(**kwargs)
        #initial=super(Ownerreg, self).get_initial()
        initial['pid'] = pid
        initial['oid']=self.request.session['oid']
        initial['oname']=self.request.session['oname']
        return  initial


class Viewproperty(ListView):
    template_name = "list_property.html"
    form_class = Propertyform
    context_object_name = "a"

def proplist(request):
    a=Property.objects.filter(rights='NS')
    return render(request,"list_property.html",{"a":a})

def Bargain(request,pid,price,oid):

    bids=request.session['bid']
    if Brqst.objects.filter(bid=bids,pid=pid).exists():
        return  HttpResponse("already ")
    else:

        brec=Buyerreg.objects.filter(bid=bids)
        for i in brec:
            bname=i.bname
        max_rqno=Brqst.objects.aggregate(max_rqno=Coalesce(Max('rqno'),Value(0)))['max_rqno']
        rqno=int(max_rqno)+1
        rqdate=date.today()
        if request.method=="POST":
            qp=request.POST.get('t1')
            sa=Brqst(rqno=rqno,rqdate=rqdate,bid=bids,bname=bname,pid=pid,price=price,qprice=qp,rights="N",oid=oid)
            sa.save()
            return render(request,"buyer_home.html")
        else:
            return render(request,"request.html",{"rqno":rqno,"rqdate":rqdate,"pid":pid,"bids":bids,"bname":bname,"price":price})

class Purchaseview(CreateView):
    template_name = "purchase.html"
    form_class = Purchaseform
    success_url = "/"

class Buyerviewresponse(ListView):
    model = Brqst
    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        context['object_list']=Brqst.objects.filter(oid=self.request.session['oid'],rights='N')
        return context

def accept(request,rqno):
    Brqst.objects.filter(rqno=rqno).update(rights='A')
    return redirect('/acc/')

class Bresponse(ListView):
    model = Brqst
    template_name = "bresponse.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Brqst.objects.filter(bid=self.request.session['bid'])
        return context
def buynow(request,rqno,pid,bid,oid,price,qprice):
    brec=Buyerreg.objects.filter(bid=bid)
    for i in brec:
        bname = i.bname
    max_pno = Purchase.objects.aggregate(max_pno=Coalesce(Max('pno'), Value(0)))['max_pno']
    pno = int(max_pno) + 1
    pdate = date.today()
    if request.method == "POST":
        qp = request.POST.get('t1')
        sa =Purchase(pno=pno,pdate=pdate, bid=bid, bname=bname, pid=pid, price=price, amtpaid=qprice , oid=oid,rqno=rqno,cardno=qp)
        sa.save()
        Brqst.objects.filter(pid=pid).delete()
        Property.objects.filter(pid=pid).update(rights="SOLD")
        return render(request, "buyer_home.html")
    else:
        return render(request, "purchases.html",
                {"pno": pno, "pdate": pdate, "bid": bid, "bname": bname, "pid": pid, "price": price, "qprice":qprice,"oid":oid,"rqno":rqno})

def buynown(request,pid,oid,price):
    bid=request.session['bid']
    brec=Buyerreg.objects.filter(bid=bid)
    for i in brec:
        bname = i.bname
    max_pno = Purchase.objects.aggregate(max_pno=Coalesce(Max('pno'), Value(0)))['max_pno']
    pno = int(max_pno) + 1
    pdate = date.today()
    if request.method == "POST":
        qp = request.POST.get('t1')
        sa =Purchase(pno=pno,pdate=pdate, bid=bid, bname=bname, pid=pid, price=price, amtpaid=price , oid=oid,cardno=qp)
        sa.save()
        Brqst.objects.filter(pid=pid).delete()
        Property.objects.filter(pid=pid).update(rights="SOLD")
        return render(request, "buyer_home.html")
    else:
        return render(request,'purchasess.html',{"pno":pno,"pdate":pdate,"bid":bid,"bname":bname,"pid":pid,"price":price,"amtpaid":price,"oid":oid})
def searchproperty(request):
    arec=Property.objects.values('ptype').distinct()
    erec=Property.objects.values('ttype').distinct()
    brec=Property.objects.values('otype').distinct()
    crec=Property.objects.values('district').distinct()
    drec=Property.objects.values('town').distinct()
    frec=Property.objects.values('pincode').distinct()
    if request.method=="POST":
        a=request.POST.get('ptype')
        b=request.POST.get('ttype')
        c=request.POST.get('otype')
        d=request.POST.get('district')
        e=request.POST.get('town')
        f=request.POST.get('pincode')
        result=Property.objects.filter(ptype=a,ttype=b,otype=c,district=d,town=e,pincode=f)
        return render(request,'searchp.html',{"result":result})
    else:
         return render(request,'searchp.html',{"arec":arec,"erec":erec,"brec":brec,"crec":crec,"drec":drec,"frec":frec})
