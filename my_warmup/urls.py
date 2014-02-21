from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from logincounter.views import login_or_add, user_add, users_login, call_resetFixture, call_unitTests

from my_warmup.view import home
from my_warmup import view


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_warmup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^hello/$', hello),
    #url(r'^display/$', display_meta),
    #url(r'^admin/$', include(admin.site.urls)), 
    
    url(r'^home/$', home),
    url(r'^search/$', login_or_add),
    url(r'^users/add$', user_add),
    url(r'^users/login$', users_login),
    url(r'^TESTAPI/resetFixture$', call_resetFixture),
    url(r'^TESTAPI/unitTests$', call_unitTests),
)


#APPEND_SLASH = True