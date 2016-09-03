"""glasses_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from myApp import views as my_app_views

urlpatterns = [
    url(r'^home', my_app_views.home, name='home'),
    url(r'^login_page', my_app_views.login_page, name='login_page'),
    url(r'^login', my_app_views.login, name='login'),
    url(r'^logout/', my_app_views.logout, name='logout'),
    url(r'^products_list/$', my_app_views.products_list, name='products_list'),
    url(r'^products_detail/$', my_app_views.products_detail, name='products_detail'),
    url(r'^download/(.+)/(.+)/(.+)', my_app_views.file_download, name='file_download'),
    url(r'^collect/(.+)', my_app_views.collect_manage, name='love'),
    url(r'^collects', my_app_views.show_collects, name='show_collects'),
    url(r'^admin_login/', my_app_views.admin_login, name='admin_login'),
    url(r'^admin_change', my_app_views.admin_change, name='admin_change'),
    url(r'^admin_logout/', my_app_views.admin_logout, name='admin_logout'),
    url(r'^get_data/(.+)', my_app_views.get_data, name='get_data'),
    url(r'^admin/user/(.+)', my_app_views.admin_member, name='admin_user'),
    url(r'^admin/home/(.+)', my_app_views.admin_home_manage, name='home_manage'),
    url(r'^admin/frame', my_app_views.admin_frame, name='bottom'),
    url(r'^admin/listTop', my_app_views.admin_list_top, name='listTop'),
    url(r'^admin/delete_member/', my_app_views.admin_delete_member, name='delete_member'),
    url(r'^admin/text_edit/(.+)/(.+)', my_app_views.admin_text_edit, name='text_edit'),
    url(r'^admin/img_edit/(.+)/(.+)', my_app_views.admin_image_edit, name='image_edit'),
    url(r'^admin/products/(.+)/(.+)/(.+)/(.+)/(.+)', my_app_views.admin_products_change, name='products_change'),
    url(r'^admin/products_type_add', my_app_views.admin_products_type_add, name='add_type'),
    url(r'^admin/products_type_delete', my_app_views.admin_products_type_delete, name='delete_type'),
    url(r'^admin/products_kind_delete', my_app_views.admin_products_kind_delete, name='delete_kind'),
    url(r'^admin/products_kind_add', my_app_views.admin_products_kind_add, name="add_kind"),
    url(r'^admin/', my_app_views.admin, name='admin'),
    url(r'^users_excel/', my_app_views.users_excel, name='admin'),
    url(r'^$', my_app_views.home),
]
