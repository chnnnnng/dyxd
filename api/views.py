import datetime

import requests, geopy, geopy.distance
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.conf import settings

from .models import User, Checkinbook, Roster, Checkinsheet, Location, Checkinitem, UserIdentitycodeCheckinsheetBond, \
    Password, Display, Wifilist
from .utils.rsps import Rsps


def index(request):
    return HttpResponse("Hello world!");


def login(request):
    code = request.GET.get('code')
    res = requests.get(
        'https://api.weixin.qq.com/sns/jscode2session?appid=' + settings.WX_APPID + '&secret=' + settings.WX_APPSECRET + '&js_code=' + code + '&grant_type=authorization_code').json()
    try:
        openid = res['openid']
        session_key = res['session_key']
    except:
        return JsonResponse(Rsps(0, '登陆失败').make())
    else:
        try:
            u = User.objects.get(openid=openid)
            if u.status == 0:
                return JsonResponse(Rsps(10, '请先完善信息', openid).make())
            else:
                return JsonResponse(Rsps(1, '登陆成功', u.getData()).make())
        except:
            n = User()
            n.openid = res['openid']
            n.session_key = res['session_key']
            n.status = 0
            n.save()
            return JsonResponse(Rsps(10, '第一次登陆，请先完善相关信息', res['openid']).make())


def setUserDetail(request):
    openid = request.GET.get('openid')
    name = request.GET.get('name')
    try:
        u = User.objects.get(openid=openid)
        u.name = name
        u.status = 1
        u.save()
        return JsonResponse(Rsps(1, '成功', {'id': u.id, 'phone': None, 'name': name}).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def createCheckinSheet(request):
    try:
        user = request.GET.get('user')
        name = request.GET.get('name')
        isInBook = request.GET.get('isInBook')
        if isInBook == 'true':
            book = request.GET.get('book')
            roster = Checkinbook.objects.get(id=book).roster
            totalnum = len(roster.getRosterData())
            n = Checkinsheet()
            n.name = name
            n.user = User.objects.get(id=user)
            n.roster = roster
            n.checkinbook = Checkinbook.objects.get(id=book)
            n.bt_address = ''
            n.num_should = totalnum
            n.save()
            for identity_code in roster.getRosterData():
                newCheckinitem = Checkinitem()
                newCheckinitem.checkinsheet = n
                newCheckinitem.identity_code = identity_code
                newCheckinitem.save()
            return JsonResponse(Rsps(1, '成功', {'id': n.id}).make())
        else:
            rosterid = request.GET.get('roster')
            roster = Roster.objects.get(id=rosterid)
            totalnum = len(roster.getRosterData())
            n = Checkinsheet()
            n.name = name
            n.user = User.objects.get(id=user)
            n.roster = roster
            n.num_should = totalnum
            n.save()
            for identity_code in roster.getRosterData():
                newCheckinitem = Checkinitem()
                newCheckinitem.checkinsheet = n
                newCheckinitem.identity_code = identity_code
                newCheckinitem.save()
            return JsonResponse(Rsps(1, '成功', {'id': n.id}).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def getBookAndRoster(request):
    try:
        user = request.GET.get('user')
        roster = Roster.objects.filter(user=user).values('id', 'name').order_by('-id')
        book = Checkinbook.objects.filter(user=user, status=0).values('id', 'name').order_by('-id')
        con = {'roster': list(roster), 'book': list(book)}
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def getCheckinsheet(request):
    try:
        checkinsheetid = request.GET.get('checkinsheet')
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        con = {
            'checkinsheet': checkinsheet.getData(),
            'checkinbook': checkinsheet.checkinbook.getData() if checkinsheet.checkinbook is not None else None,
            'roster': checkinsheet.roster.getRosterInfo()
        }
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def getCreated(request):
    try:
        user = request.GET.get('user')
        checkinsheet = Checkinsheet.objects.filter(user=user).values('id', 'name', 'roster', 'checkinbook',
                                                                     'status').order_by('-id')
        checkinbook = Checkinbook.objects.filter(user=user).values('id', 'name', 'status').order_by('-id')
        roster = Roster.objects.filter(user=user).values('id', 'name').order_by('-id')
        con = {'checkinsheet': list(checkinsheet), 'checkinbook': list(checkinbook), 'roster': list(roster)}
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def getCheckinbook(request):
    try:
        checkinbookid = request.GET.get('checkinbook')
        checkinbook = Checkinbook.objects.get(id=checkinbookid)
        checkinsheet = Checkinsheet.objects.filter(checkinbook=checkinbook).values('id', 'name', 'status').order_by(
            '-id')
        con = {
            'checkinbook': checkinbook.getData(),
            'checkinsheet': list(checkinsheet),
            'roster': checkinbook.roster.getRosterInfo()
        }
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def getRoster(request):
    try:
        rosterid = request.GET.get('roster')
        roster = Roster.objects.get(id=rosterid)
        con = {'info': roster.getRosterInfo(), 'roster': roster.getRosterData()}
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def createCheckinbook(request):
    try:
        user = request.GET.get('user')
        rosterid = request.GET.get('roster')
        name = request.GET.get('name')
        n = Checkinbook()
        n.user = User.objects.get(id=user)
        n.roster = Roster.objects.get(id=rosterid)
        n.name = name
        n.save()
        return JsonResponse(Rsps(1, '成功', n.id).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def createRoster(request):
    try:
        user = request.GET.get('user')
        rosterstr = request.GET.get('roster')
        name = request.GET.get('name')
        n = Roster()
        n.user = User.objects.get(id=user)
        n.name = name
        n.roster = rosterstr
        n.save()
        return JsonResponse(Rsps(1, '成功', {'id': n.id}).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def deleteRoster(request):
    try:
        rosterid = request.GET.get('roster')
        roster = Roster.objects.get(id=rosterid)
        roster.delete()
        return JsonResponse(Rsps(1, '删除成功').make())
    except:
        return JsonResponse(Rsps(0, '无法删除').make())


def deleteCheckinbook(request):
    try:
        checkinbookid = request.GET.get('checkinbook')
        checkinbook = Checkinbook.objects.get(id=checkinbookid)
        checkinbook.delete()
        return JsonResponse(Rsps(1, '删除成功').make())
    except:
        return JsonResponse(Rsps(0, '无法删除').make())


def deleteCheckinsheet(request):
    try:
        checkinsheetid = request.GET.get('checkinsheet')
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        checkinsheet.delete()
        return JsonResponse(Rsps(1, '删除成功').make())
    except:
        return JsonResponse(Rsps(0, '无法删除').make())


def exposeLocation(request):
    try:
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')
        radius = request.GET.get('radius')
        checkinsheetid = request.GET.get('checkinsheet')
        type = request.GET.get('type', 1)
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        n = Location()
        n.longitude = longitude
        n.latitude = latitude
        n.radius = radius
        n.checkinsheet = checkinsheet
        n.type = type
        n.save()
        checkinsheet.type = type
        checkinsheet.save()
        return JsonResponse(Rsps(1, '成功', {'locationid': n.id}).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def unexposeLocation(request):
    try:
        locationid = request.GET.get('locationid', None)
        checkinsheetid = request.GET.get('checkinsheetid', None)
        if checkinsheetid is None:
            n = Location.objects.get(id=locationid)
            n.checkinsheet.type = 5
            n.checkinsheet.save()
            n.delete()
            return JsonResponse(Rsps(1, '删除成功').make())
        else:
            n = Location.objects.get(checkinsheet=Checkinsheet.objects.get(id=checkinsheetid))
            n.checkinsheet.type = 5
            n.checkinsheet.save()
            n.delete()
            return JsonResponse(Rsps(1, '删除成功').make())
    except:
        return JsonResponse(Rsps(0, '无法删除').make())


def getLocation(request):
    try:
        locationid = request.GET.get('locationid', None)
        checkinsheetid = request.GET.get('checkinsheet', None)
        if checkinsheetid is None:
            n = Location.objects.get(id=locationid)
            return JsonResponse(Rsps(1, '成功', n.getData()).make())
        else:
            n = Location.objects.get(checkinsheet=Checkinsheet.objects.get(id=checkinsheetid))
            return JsonResponse(Rsps(1, '成功', n.getData()).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def discover(request):
    try:
        lat = request.GET.get('latitude')
        long = request.GET.get('longitude')
        center = geopy.Point(int(lat) / 1000000, int(long) / 1000000)
        dis = geopy.distance.VincentyDistance(kilometers=1.5)
        # 框出一个边长3km的矩形
        minlat = round(dis.destination(point=center, bearing=180).latitude * 1000000)
        maxlat = round(dis.destination(point=center, bearing=0).latitude * 1000000)
        minlong = round(dis.destination(point=center, bearing=270).longitude * 1000000)
        maxlong = round(dis.destination(point=center, bearing=90).longitude * 1000000)
        res = Location.objects.filter(latitude__lt=maxlat, latitude__gt=minlat, longitude__lt=maxlong,
                                      longitude__gt=minlong)
        res_1 = []
        for i in res:
            actual_distance = geopy.distance.distance((i.latitude / 1000000, i.longitude / 1000000), center).m
            if actual_distance <= i.radius * 1.5:  # 宽容一些防止查不到
                res_1.append({'distance': actual_distance, 'checkinsheet': i.checkinsheet.getData(), 'type': i.type})
        return JsonResponse(Rsps(1, '成功', res_1).make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def getIdentitycode(request):
    try:
        userid = request.GET.get('user')
        checkinsheetid = request.GET.get('checkinsheet')
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        if checkinsheet.checkinbook is None:
            return JsonResponse(Rsps(0, '无结果').make())
        else:
            a = UserIdentitycodeCheckinsheetBond.objects.get(user=User.objects.get(id=userid),
                                                             checkinbook=checkinsheet.checkinbook)
            return JsonResponse(Rsps(1, '成功', a.identity_code).make())
    except:
        return JsonResponse(Rsps(0, '无结果').make())


def putCheckin(request):
    userid = request.GET.get('user')
    checkinsheetid = request.GET.get('checkinsheet')
    identity_code = request.GET.get('identity_code')
    try:
        user = User.objects.get(id=userid)
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        roster = checkinsheet.roster.getRosterData()
        if identity_code not in roster:
            return JsonResponse(Rsps(0, '身份认证失败').make())
        if checkinsheet.checkinbook is not None:
            try:
                n = UserIdentitycodeCheckinsheetBond.objects.get(user=user, checkinbook=checkinsheet.checkinbook)
            except:
                n = UserIdentitycodeCheckinsheetBond()
                n.user = user
                n.checkinbook = checkinsheet.checkinbook
                n.identity_code = identity_code
                n.save()
            if n.identity_code != identity_code:
                return JsonResponse(Rsps(0, '身份认证失败').make())
            try:
                a = Checkinitem.objects.get(checkinsheet=checkinsheet, identity_code=identity_code)
                a.user = user
                if a.status == 0:
                    a.status = 1
                    a.save()
                    checkinsheet.num_actual += 1
                    checkinsheet.save()
                    return JsonResponse(Rsps(1, '成功').make())
                elif a.status == 1:
                    return JsonResponse(Rsps(0, '已签到无需再次签到').make())
                elif a.status == 2:
                    return JsonResponse(Rsps(0, '已请假无需签到').make())
                else:
                    return JsonResponse(Rsps(0, '签到已过期').make())
            except:
                return JsonResponse(Rsps(0, '身份认证失败').make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def setCheckinsheetStatus(request):
    checkinsheetid = request.GET.get('checkinsheet')
    status = True if request.GET.get('status') == 'true' else False
    try:
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        if (checkinsheet.status == False) and (status == True):  # 原来是未完结，要改为已完结
            if checkinsheet.type == 0:  # 有快签
                Wifilist.objects.filter(checkinsheet=checkinsheet).delete()
            if checkinsheet.type <= 1:  # 有location信息
                Location.objects.get(checkinsheet=checkinsheet).delete()
            if checkinsheet.type == 2:  # 有扫码
                Display.objects.get(checkinsheet=checkinsheet).delete()
            if checkinsheet.type == 3:  # 有口令
                Password.objects.get(checkinsheet=checkinsheet).delete()
            checkinsheet.num_absent = checkinsheet.num_should - checkinsheet.num_actual - checkinsheet.num_leave
            checkinsheet.attendance_rate = (checkinsheet.num_actual + checkinsheet.num_leave) / checkinsheet.num_should
            checkinsheet.status = True
            checkinsheet.type = 5
            checkinsheet.save()
            checkinitems = Checkinitem.objects.filter(checkinsheet=checkinsheet, status=0)
            for checkinitem in checkinitems:
                try:
                    checkinitem.user = UserIdentitycodeCheckinsheetBond.objects.get(
                        checkinbook=checkinsheet.checkinbook,
                        identity_code=checkinitem.identity_code).user
                except:
                    checkinitem.user = None
                checkinitem.status = 3
                checkinitem.save()
            return JsonResponse(Rsps(1, '成功').make())
        elif (checkinsheet.status == True) and (status == False):  # 关->开,要保证其父级是开的
            if checkinsheet.checkinbook_id is None or checkinsheet.checkinbook.status == False:
                checkinsheet.num_absent = 0
                checkinsheet.status = False
                checkinsheet.attendance_rate = 0
                checkinsheet.save()
                checkinitems = Checkinitem.objects.filter(checkinsheet=checkinsheet, status=3)
                for checkinitem in checkinitems:
                    checkinitem.status = 0
                    checkinitem.save()
                return JsonResponse(Rsps(1, '成功').make())
            else:
                return JsonResponse(Rsps(0, '操作失败，因为其父级点名册已完结').make())
        else:
            return JsonResponse(Rsps(0, '操作失败').make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def setCheckinbookStatus(request):
    checkinbookid = request.GET.get('checkinbook')
    status = True if request.GET.get('status') == 'true' else False
    try:
        checkinbook = Checkinbook.objects.get(id=checkinbookid)
        if (checkinbook.status == False) and (status == True):  # 开->关
            checkinbook.status = True
            checkinbook.save()
            checkinsheets = Checkinsheet.objects.filter(checkinbook=checkinbook, status=False)
            for checkinsheet in checkinsheets:
                if checkinsheet.type == 0:  # 有快签
                    Wifilist.objects.filter(checkinsheet=checkinsheet).delete()
                if checkinsheet.type <= 1:  # 有location信息
                    Location.objects.get(checkinsheet=checkinsheet).delete()
                if checkinsheet.type == 2:  # 有扫码
                    Display.objects.get(checkinsheet=checkinsheet).delete()
                if checkinsheet.type == 3:  # 有口令
                    Password.objects.get(checkinsheet=checkinsheet).delete()
                checkinsheet.num_absent = checkinsheet.num_should - checkinsheet.num_actual - checkinsheet.num_leave
                checkinsheet.attendance_rate = (
                                                       checkinsheet.num_actual + checkinsheet.num_leave) / checkinsheet.num_should
                checkinsheet.status = True
                checkinsheet.type = 5
                checkinsheet.save()
                checkinitems = Checkinitem.objects.filter(checkinsheet=checkinsheet, status=0)
                for checkinitem in checkinitems:
                    try:
                        checkinitem.user = UserIdentitycodeCheckinsheetBond.objects.get(checkinsheet=checkinbook,
                                                                                        identity_code=checkinitem.identity_code).user
                    except:
                        checkinitem.user = None
                    checkinitem.status = 3
                    checkinitem.save()
            return JsonResponse(Rsps(1, '成功').make())
        elif (checkinbook.status == True) and (status == False):  # 关->开
            checkinbook.status = False
            checkinbook.save()
            return JsonResponse(Rsps(1, '成功').make())
        else:
            return JsonResponse(Rsps(0, '操作失败').make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def getCheckinitems(request):
    try:
        checkinsheetid = request.GET.get('checkinsheet')
        checkinitems = Checkinitem.objects.filter(checkinsheet=Checkinsheet.objects.get(id=checkinsheetid))
        res = []
        for checkinitem in checkinitems:
            res.append(checkinitem.getData())
        return JsonResponse(Rsps(1, '成功', res).make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def setCheckinitemStatus(request):
    checkinitemid = request.GET.get('checkinitem')
    status = int(request.GET.get('status'))
    try:
        checkinitem = Checkinitem.objects.get(id=checkinitemid)
        oldStatus = checkinitem.status
        checkinitem.status = status
        checkinitem.save()
        if oldStatus == 1:
            checkinitem.checkinsheet.num_actual -= 1
        if oldStatus == 2:
            checkinitem.checkinsheet.num_leave -= 1
        if oldStatus == 3:
            checkinitem.checkinsheet.num_absent -= 1
        if status == 1:
            checkinitem.checkinsheet.num_actual += 1
        if status == 2:
            checkinitem.checkinsheet.num_leave += 1
        if status == 3:
            checkinitem.checkinsheet.num_absent += 1
        checkinitem.checkinsheet.attendance_rate = (
                                                           checkinitem.checkinsheet.num_actual + checkinitem.checkinsheet.num_leave) / checkinitem.checkinsheet.num_should
        checkinitem.checkinsheet.save()
        return JsonResponse(Rsps(1, '成功').make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def getCheckinbookData(request):
    try:
        checkinbookid = request.GET.get('checkinbook')
        con = {'checkinbook': {}, 'checkinsheet': [], 'roster': []}
        checkinbook = Checkinbook.objects.get(id=checkinbookid)
        con['checkinbook'] = checkinbook.getData()
        checkinsheets = Checkinsheet.objects.filter(checkinbook=checkinbook)
        for checkinsheet in checkinsheets:
            t = checkinsheet.getData()
            t['checkinitems'] = []
            checkinitems = Checkinitem.objects.filter(checkinsheet=checkinsheet)
            for checkinitem in checkinitems:
                t['checkinitems'].append(checkinitem.getData())
            con['checkinsheet'].append(t)
        con['roster'] = {'info': checkinbook.roster.getRosterInfo(), 'data': checkinbook.roster.getRosterData()}
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def getPasswordInfo(request):
    passwords = request.GET.get('password', None)
    checkinsheetid = request.GET.get('checkinsheet', None)
    if checkinsheetid is None:
        try:
            password = Password.objects.get(password=int(passwords) + 10000)
            return JsonResponse(Rsps(1, '成功', password.checkinsheet.getData()).make())
        except:
            return JsonResponse(Rsps(0, '口令不存在').make())
    else:
        try:
            checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
            password = Password.objects.get(checkinsheet=checkinsheet)
            return JsonResponse(
                Rsps(1, '成功',
                     {'password': str(password.password)[1:5], 'checkinsheet': password.checkinsheet.getData()}).make())
        except:
            return JsonResponse(Rsps(0, '口令不存在').make())


def setPassword(request):
    try:
        passwords = request.GET.get('password')
        checkinsheetid = request.GET.get('checkinsheet')
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        if checkinsheet.type != 5:
            return JsonResponse(Rsps(0, '已有其他签到方式').make())
        else:
            try:
                Password.objects.get(checkinsheet=checkinsheet)
                return JsonResponse(Rsps(0, '此口令与现存口令冲突，请换一个试试').make())
            except:
                n = Password()
                n.password = 10000 + int(passwords)
                n.checkinsheet = checkinsheet
                n.save()
                checkinsheet.type = 3
                checkinsheet.save()
                return JsonResponse(Rsps(1, '成功').make())

    except:
        return JsonResponse(Rsps(0, '失败').make())


def deletePassword(request):
    passwords = request.GET.get('password', None)
    checkinsheetid = request.GET.get('checkinsheet', None)
    if checkinsheetid is None:
        try:
            password = Password.objects.get(password=int(passwords) + 10000)
            password.checkinsheet.type = 5
            password.checkinsheet.save()
            password.delete()
            return JsonResponse(Rsps(1, '成功').make())
        except:
            return JsonResponse(Rsps(0, '口令不存在').make())
    else:
        try:
            checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
            checkinsheet.type = 5
            checkinsheet.save()
            password = Password.objects.get(checkinsheet=checkinsheet)
            password.delete()
            return JsonResponse(Rsps(1, '成功').make())
        except:
            return JsonResponse(Rsps(0, '口令不存在').make())


def getHistory(request):
    try:
        userid = request.GET.get('user')
        checkinitems = Checkinitem.objects.filter(user=User.objects.get(id=userid))
        con = []
        for checkinitem in checkinitems:
            con.append({
                'checkinsheet_name': checkinitem.checkinsheet.name,
                'checkinsheet_user_name': checkinitem.checkinsheet.user.name,
                'checkinitem_time': checkinitem.time,
                'checkinitem_status': checkinitem.status,
            })
        return JsonResponse(Rsps(1, '成功', con).make())
    except:
        return JsonResponse(Rsps(0, '失败').make())


def display(request):
    action = request.GET.get('action', None)
    if action is None:
        displayID = request.COOKIES.get('displayID', -1)
        rep = render(request, 'display.html')
        try:
            n = Display.objects.get(id=displayID)
            rep.set_cookie('displayID', n.id)
        except:
            n = Display()
            n.save()
            rep.set_cookie('displayID', n.id)
        return rep
    elif action == 'check':
        displayID = request.COOKIES.get('displayID', None)
        display = Display.objects.get(id=displayID)
        return JsonResponse(Rsps(1, '成功',
                                 None if display.checkinsheet is None else {'checkinsheet_id': display.checkinsheet.id,
                                                                            'checkinsheet_name': display.checkinsheet.name,
                                                                            'time': display.time.strftime(
                                                                                "%Y-%m-%d %H:%M:%S.%f")}).make())
    elif action == 'regist':
        displayID = request.GET.get('displayID', None)
        checkinsheetid = request.GET.get('checkinsheet', None)
        try:
            checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
            display = Display.objects.get(id=displayID)
            display.checkinsheet = checkinsheet
            display.status = 1
            display.save()
            checkinsheet.type = 2
            checkinsheet.save()
            return JsonResponse(Rsps(1, '成功', display.id).make())
        except:
            return JsonResponse(Rsps(0, '失败').make())
    elif action == 'cancel':
        checkinsheetid = request.GET.get('checkinsheet', None)
        try:
            checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
            display = Display.objects.get(checkinsheet=checkinsheet)
            display.checkinsheet = None
            display.status = 0
            display.save()
            checkinsheet.type = 5
            checkinsheet.save()
            return JsonResponse(Rsps(1, '成功', display.id).make())
        except:
            return JsonResponse(Rsps(0, '失败').make())
    elif action == 'check2':
        displayID = request.COOKIES.get('displayID', None)
        lastTime = request.GET.get('lasttime')
        display = Display.objects.get(id=displayID)
        if display.status == 0:
            return JsonResponse(Rsps(0, '已结束').make())
        else:
            checkinitems = Checkinitem.objects.filter(checkinsheet=display.checkinsheet, time__gt=lastTime)
            con = []
            for checkinitem in checkinitems:
                con.append({
                    'user_name': checkinitem.user.name,
                    'user_identity_code': checkinitem.identity_code,
                    'time': checkinitem.time.strftime("%Y-%m-%d %H:%M:%S.%f")
                })
            return JsonResponse(Rsps(1, '进行中', con).make())


def checkinTest(request):
    checkinsheetid = request.GET.get('checkinsheet')
    checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
    checninitems = Checkinitem.objects.filter(status=0, checkinsheet=checkinsheet)
    checkinitem = checninitems[0]
    checkinitem.user_id = 12
    checkinitem.status = 1
    checkinitem.save()
    checkinsheet.num_actual += 1
    checkinsheet.save()
    return JsonResponse(Rsps(1, '').make())


def setLink(request):
    checkinsheetid = request.GET.get('checkinsheet')
    try:
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        checkinsheet.type = 4
        checkinsheet.save()
        return JsonResponse(Rsps(1, '链接已开放').make())
    except:
        return JsonResponse(Rsps(0, '开放链接失败').make())


def deleteLink(request):
    checkinsheetid = request.GET.get('checkinsheet')
    try:
        checkinsheet = Checkinsheet.objects.get(id=checkinsheetid)
        checkinsheet.type = 5
        checkinsheet.save()
        return JsonResponse(Rsps(1, '链接已关闭').make())
    except:
        return JsonResponse(Rsps(0, '关闭链接失败').make())


def userinfo(request):
    userid = request.GET.get('userid', None)
    realname = request.GET.get('realname', None)
    phone = request.GET.get('phone', None)
    openid = request.GET.get('openid', None)
    try:
        if openid is not None:
            user = User.objects.get(id=userid, openid=openid)
            user.delete()
            return JsonResponse(Rsps(1, '').make())
        elif realname is None and phone is None:  # GET
            user = User.objects.get(id=userid)
            return JsonResponse(Rsps(1, '', {'realname': user.name, 'phone': user.phone}).make())
        else:
            user = User.objects.get(id=userid)
            if realname is not None:
                user.name = realname
            if phone is not None:
                user.phone = phone
            user.save()
            return JsonResponse(Rsps(1, '').make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def pushWifilist(request):
    try:
        checkinsheet = Checkinsheet.objects.get(id=(request.GET.get('checkinsheet')))
        user = User.objects.get(id=(request.GET.get('user')))
        type = bool(request.GET.get('type', 0))
        wifilist = request.GET.get('wifilist')
        n = Wifilist()
        n.checkinsheet = checkinsheet
        n.user = user
        n.type = type
        n.wifilist = wifilist
        n.save()
        return JsonResponse(Rsps(1, '').make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def pullWifilist(request):
    try:
        checkinsheet = Checkinsheet.objects.get(id=(request.GET.get('checkinsheet')))
        wifilists = Wifilist.objects.filter(checkinsheet=checkinsheet).values('wifilist')
        return JsonResponse(Rsps(1, '', list(wifilists)).make())
    except:
        return JsonResponse(Rsps(0, '操作失败').make())


def getF2fInfo(request):
    checkinsheet = Checkinsheet.objects.get(id=(request.GET.get('checkinsheet')))
    if checkinsheet.type == 5:
        return JsonResponse(Rsps(1, '一切正常', checkinsheet.getData()).make())
    else:
        Location.objects.filter(checkinsheet=checkinsheet).delete()
        Wifilist.objects.filter(checkinsheet=checkinsheet).delete()
        checkinsheet.type = 5
        checkinsheet.save()
        return JsonResponse(Rsps(0, '检测到上次异常退出，已为您关闭面对面快签，现在可以重新发起', checkinsheet.getData()).make())


def pullCheckinInfo(request):
    checkinsheet = Checkinsheet.objects.get(id=(request.GET.get('checkinsheet')))
    return JsonResponse(Rsps(1, '抓取成功', checkinsheet.getData()).make())


def startF2f(request):
    checkinsheet = Checkinsheet.objects.get(id=(request.GET.get('checkinsheet')))
    if Location.objects.filter(checkinsheet=checkinsheet).count() > 0 and Wifilist.objects.filter(
            checkinsheet=checkinsheet).count() > 0:
        checkinsheet.type = 0
        checkinsheet.save()
        return JsonResponse(Rsps(1, '成功').make())
    else:
        return JsonResponse(Rsps(0, '网络连接异常，请退出后重试').make())


def stopF2f(request):
    checkinsheet = Checkinsheet.objects.get(id=(request.GET.get('checkinsheet')))
    Location.objects.filter(checkinsheet=checkinsheet).delete()
    Wifilist.objects.filter(checkinsheet=checkinsheet).delete()
    checkinsheet.type = 5
    checkinsheet.save()
    return JsonResponse(Rsps(1, '成功').make())
