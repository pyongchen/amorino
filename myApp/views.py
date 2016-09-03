# coding=utf-8
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from myApp.manager.member_manager import memberManager
from myApp.manager.excel_manager import excelManager
from myApp.manager.login_manager import loginManager
from myApp import models
from myApp.manager.admin_edit_manager import adminEditManager
from myApp.manager.collect_manager import collectManager
from myApp.manager.download_manager import downloadManager
from myApp.manager.frame_manager import frameManager
from myApp.manager.home_manager import homeManager
from myApp.manager.response_data_manager import responseDataManager


# Create your views here.


def home(request):
    print request.META['HTTP_USER_AGENT'].lower().find('mobile')
    return render_to_response('client/pc/home.html', {
                    'title': 'Amorino'}
                              )


def logout(request):
    username = request.session.get('username')
    response = render_to_response('client/pc/home.html', {
        'title': 'Amorino'}
                                  )
    if username:
        loginManager.log_out(username)
        del request.session['username']
    return response


def login(request):
    if request.method == 'POST':
        return HttpResponse(loginManager.login(request),
                            content_type="application/json")
    else:
        username = request.session.get('username')
        return HttpResponse(username)


def products_list(request):
    username = request.session.get('username')
    return render_to_response('client/pc/products_list.html', {
        'errMess': 'None',
        'title': 'Products',
        'username': str(username)
    })


def products_detail(request):
    username = str(request.session.get('username'))
    if username == 'None':
        return HttpResponse({
            'errMess': '请先登录才可浏览产品大图',
            'username': str(username)
        })
    else:
        return render_to_response('client/pc/products_detail.html', {
            'username': username,
            'title': 'Products'
        })


def admin_login(request):
    if request.session.get('admin_username'):
        return HttpResponseRedirect('/admin')
    else:
        return render_to_response('admin/admin_login.html')


def admin(request):
    if request.method == 'POST':
        result = loginManager.admin_login(request)
        if result != 0:
            request.session['admin_username'] = result['username']
            return render_to_response('admin/admin.html', loginManager.get_admin(''))
        else:
            return render_to_response('admin/admin_login.html', {
                'errMess': '用户名或密码错误'
            })
    else:
        username = request.session.get('admin_username')
        if username:
            return render_to_response('admin/admin.html', loginManager.get_admin(''))
        else:
            return HttpResponseRedirect('/admin_login')


def admin_logout(request):
    response = render_to_response('admin/admin_login.html')
    if request.session.get('admin_username'):
        del request.session['admin_username']
    return response


def admin_change(request):
    loginManager.admin_change(request)
    return render_to_response('admin/admin.html', loginManager.get_admin(''))


def admin_member(request, operate):
    operate = str(operate)
    return HttpResponse(memberManager.operate(json.loads(request.body), operate),
                        content_type="application/json")


def admin_delete_member(request):
    username = request.POST['username']
    if username:
        if memberManager.delete_members(username) == 1:
            models.Member.objects.filter(username=username).delete()
            info = '删除用户成功'
        else:
            info = '用户名不存在'
    else:
        info = '用户名不能为空'
    return render_to_response('admin/admin.html', loginManager.get_admin(info))


def admin_home_manage(request, part):
    part = str(part)
    homeManager.update(request, part)
    return HttpResponse(json.dumps("{}"),
                        content_type="application/json")


def admin_text_edit(request, param1, param2):
    if param1 == 'home':
        adminEditManager.edit_home_text(request, param2)
    else:
        pass
    return render_to_response('admin/admin.html', responseDataManager.get_data(
        request.COOKIES['admin_username'], '修改成功'))


def admin_image_edit(request, p1, p2):
    if p1 == 'home':
        adminEditManager.edit_home_img(request, p2)
    else:
        pass
    return render_to_response('admin/admin.html', responseDataManager.get_data(
        request.COOKIES['admin_username'], ''))


def admin_products_change(request, p1, p2, p3, p4, p5):
    adminEditManager.edit_products(request, str(p1), str(p2), str(p3), str(p4), str(p5))
    return render_to_response('admin/admin.html', responseDataManager.get_data(
        request.session['admin_username'], ''))


def admin_products_kind_delete(request):
    data = json.loads(request.body)
    type_ = data['type']
    kind = data['key']
    adminEditManager.delete_products_kind(type_, kind)
    return HttpResponse(responseDataManager.admin_data(),
                        content_type="application/json")


def admin_products_kind_add(request):
    data = json.loads(request.body)
    type_ = data['type']
    kind_zh = data['kind']
    adminEditManager.add_products_kind(type_, kind_zh)
    return HttpResponse(responseDataManager.admin_data(),
                        content_type="application/json")


def admin_products_type_add(request):
    data = json.loads(request.body)
    type_ = data['type']
    adminEditManager.add_products_type(type_)
    return HttpResponse(responseDataManager.admin_data(),
                        content_type="application/json")


def admin_products_type_delete(request):
    data = json.loads(request.body)
    type_ = data['type']
    adminEditManager.delete_products_type(type_)
    return HttpResponse(responseDataManager.admin_data(),
                        content_type="application/json")


def admin_list_top(request):
    data = json.loads(request.body)
    type_ = data['type']
    kind = data['kind']
    index = data['index']
    adminEditManager.list_top(type_, kind, index)
    return HttpResponse(responseDataManager.admin_data(),
                        content_type="application/json")


def admin_frame(request):
    frameManager.update(request)
    return HttpResponse(json.dumps("{}"),
                        content_type="application/json")


def file_download(request, p1, p2, p3):
    type_ = str(p1)
    kind = str(p2)
    index = str(p3)
    path = 'static/img/products_list/' + type_ + '/' + kind + '/' + index
    response = downloadManager.download(path)
    return response


def users_excel(request):
    return excelManager.get_members()


def collect_manage(request, operate):
    data = json.loads(request.body)
    collectManager.operation(data, operate, request.session.get('username'))
    return HttpResponse(responseDataManager.user_collect_data(request),
                        content_type="application/json")


def show_collects(request):
    username = str(request.session.get('username'))
    if username == 'None':
        return HttpResponseRedirect('/home')
    else:
        return render_to_response('client/pc/collects.html', {
            'username': username,
            'title': 'Collects'
        })


def get_data(request, kind):
    if kind == 'frame':
        return HttpResponse(responseDataManager.frame_data(),
                            content_type="application/json")
    elif kind == 'base_info':
        return HttpResponse(responseDataManager.base_info(),
                            content_type="application/json")
    elif kind == 'admin':
        return HttpResponse(responseDataManager.admin_data(),
                            content_type="application/json")
    elif kind == 'home':
        return HttpResponse(responseDataManager.home_data(),
                            content_type='application/json')
    elif kind == 'collect':
        return HttpResponse(responseDataManager.user_collect_data(request),
                            content_type="application/json")
    else:
        return HttpResponse(responseDataManager.user_data(),
                            content_type="application/json")
