import json

from django.db import models


class User(models.Model):
    def __str__(self):
        return self.name

    openid = models.CharField(max_length=50)
    session_key = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11, null=True)
    status = models.BooleanField(choices=((0, '未登录'), (1, '已登陆')), default=0)

    def getData(self):
        return {'id': self.id, 'openid': self.openid, 'session_key': self.session_key, 'name': self.name,
                'phone': self.phone, 'status': self.status}


class Roster(models.Model):
    def __str__(self):
        return self.name

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    roster = models.TextField()

    def getRosterData(self):
        return json.loads(self.roster)

    def getRosterInfo(self):
        return {'id': self.id, 'name': self.name}


class Checkinbook(models.Model):
    def __str__(self):
        return self.name

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    roster = models.ForeignKey('Roster', on_delete=models.CASCADE)
    status = models.BooleanField(choices=((0, '进行中'), (1, '已关闭')), default=0)

    def getData(self):
        return {'id': self.id, 'name': self.name, 'status': self.status}


class Checkinsheet(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=20)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    roster = models.ForeignKey('Roster', on_delete=models.CASCADE)
    checkinbook = models.ForeignKey('Checkinbook', on_delete=models.CASCADE, null=True, default=None)
    bt_address = models.CharField(max_length=20, null=True)
    num_should = models.IntegerField(default=0)
    num_actual = models.IntegerField(default=0)
    num_leave = models.IntegerField(default=0)
    num_absent = models.IntegerField(default=0)
    attendance_rate = models.FloatField(default=0)
    status = models.BooleanField(choices=((0, '进行中'), (1, '已关闭')), default=0)
    type = models.IntegerField(default=5,
                               choices=((0, '面对面快签'), (1, '定位签'), (2, '扫码签'), (3, '口令签'), (4, '链接签'), (5, '无')))

    def getData(self):
        return {'id': self.id, 'name': self.name, 'bt_address': self.bt_address, 'num_should': self.num_should,
                'num_actual': self.num_actual, 'num_leave': self.num_leave
            , 'num_absent': self.num_absent, 'attendance_rate': self.attendance_rate, 'status': self.status,
                'user': self.user.name, 'type': self.type, 'type_name': self.get_type_display()}


class Checkinitem(models.Model):
    checkinsheet = models.ForeignKey('Checkinsheet', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    identity_code = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0, choices=((0, '待签'), (1, '出勤'), (2, '请假'), (3, '缺勤')))

    def getData(self):
        return {'id': self.id, 'identity_code': self.identity_code, 'status': self.status,
                'user': None if self.user is None else self.user.name}


class Location(models.Model):
    latitude = models.IntegerField(default=0)
    longitude = models.IntegerField(default=0)
    radius = models.IntegerField(default=50)
    type = models.BooleanField(choices=((0, '面对面快签'), (1, '定位签')), default=0)
    checkinsheet = models.ForeignKey('Checkinsheet', on_delete=models.CASCADE)

    def getData(self):
        return {'latitude': self.latitude, 'longitude': self.longitude, 'radius': self.radius, 'type': self.type,
                'checkinsheet': self.checkinsheet.id}


class UserIdentitycodeCheckinsheetBond(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    checkinbook = models.ForeignKey('Checkinbook', on_delete=models.CASCADE, null=True, default=None)
    identity_code = models.CharField(max_length=20)


class Password(models.Model):
    password = models.IntegerField(default=10000)
    checkinsheet = models.ForeignKey('Checkinsheet', on_delete=models.CASCADE)


class Display(models.Model):
    checkinsheet = models.ForeignKey('Checkinsheet', on_delete=models.CASCADE,null=True)
    status = models.BooleanField(choices=((0, '就绪'), (1, '进行')), default=0)
    time = models.DateTimeField(auto_now=True)


class Wifilist(models.Model):
    checkinsheet = models.ForeignKey('Checkinsheet', on_delete=models.CASCADE,null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    type = models.BooleanField(choices=((0, '目标列表'), (1, '补充列表')), default=0)
    wifilist = models.TextField()
