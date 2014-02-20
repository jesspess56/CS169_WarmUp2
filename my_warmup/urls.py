from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from logincounter.views import user_add, user_login, call_resetFixture

from my_warmup.view import login_page

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_warmup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login_page),
    url(r'^users/add$', user_add),
    url(r'^users/login$', user_login),
    url(r'^TESTAPI/resetFixture$', call_resetFixture)
    url(r'^TESTAPI/unitTests$', call_unitTests),
)


