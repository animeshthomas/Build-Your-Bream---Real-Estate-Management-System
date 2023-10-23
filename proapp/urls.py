from django.urls import path
from proapp import views
from proapp.views import Addowner,Listowner,Addbuyer,Listbuyer,Bdelete,Bedit,Odelete,Oedit,Addproperty,Viewproperty,Purchaseview,Buyerviewresponse,Bresponse

urlpatterns=[
    path('',views.home),
    path('oadd/',Addowner.as_view()),
    path('odis/',Listowner.as_view()),
    path('badd/',Addbuyer.as_view()),
    path('bdis/',Listbuyer.as_view()),
    path('rights/',views.ch),
    path('login/',views.login),
    path('bedit/<pk>',Bedit.as_view()),
    path('oedit/<pk>',Oedit.as_view()),
    path('bdelete/<pk>',Bdelete.as_view()),
    path('odelete/<pk>',Odelete.as_view()),
    path('updater/<int:oid>/',views.updaterights),
    path('oreject/<int:oid>',views.oreject),
    path('editowner/',views.editowner),
    path('updateowner/',views.updateowner),
    path('editbuyer/',views.editbuyer),
    path('updatebuyer/',views.updatebuyer),
    path('addp/',Addproperty.as_view()),
    path('disp/',Viewproperty.as_view()),
    path('pdis/',views.proplist),
    path('rqst/<int:pid>/<int:price>/<int:oid>/',views.Bargain),
    path('pur/',Purchaseview.as_view()),
    path('acc/',Buyerviewresponse.as_view()),
    path('accept/<int:rqno>/',views.accept),
    path('resp/',Bresponse.as_view()),
    path('buy/<int:rqno>/<int:pid>/<int:bid>/<int:oid>/<int:price>/<int:qprice>/',views.buynow),
    path('buyn/<int:pid>/<int:oid>/<int:price>/',views.buynown),
    path('ser/',views.searchproperty),


]