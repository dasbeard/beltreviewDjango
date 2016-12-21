from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register' ),
    url(r'^success$', views.success, name='success'),
    url(r'^signout$', views.signout, name='signout'),
]
