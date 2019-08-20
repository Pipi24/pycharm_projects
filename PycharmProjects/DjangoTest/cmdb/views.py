from django.shortcuts import render

from django.shortcuts import HttpResponse
from cmdb import models
# Create your views here.

# user_list = [
#     {"user": "shaw", "pwd": "abc"},
#     {"user": "asdgg", "pwd": "sgfd"},
# ]


def response(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        passwd = request.POST.get("password", None)
        # print(username, passwd)
        # temp = {"user": username, "pwd": passwd}
        # user_list.append(temp)
        models.UserInfo.objects.create(user=username, pwd=passwd)
    user_list = models.UserInfo.objects.all()
    return render(request, "myHtml.html", {"data": user_list})
