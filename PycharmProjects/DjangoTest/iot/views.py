from django.shortcuts import render

from iot import models
from iot import store
# Create your views here.

# user_list = [
#     {"user": "shaw", "pwd": "abc"},
#     {"user": "asdgg", "pwd": "sgfd"},
# ]


def response(request):
    # path = '/home/wuhiu/deeplearning/VPNData/non-vpn/Streaming/youtube1.pcap'
    # store.store_fields(path)

    if request.method == 'POST':
        sourceIP = request.POST.get("SourceIP", None)
        distIP = request.POST.get("DistIP", None)
        count = request.POST.get('count', None)
        # print(username, passwd)
        # temp = {"user": username, "pwd": passwd}
        # user_list.append(temp)
        models.IOTTest.objects.create(sourceIP=sourceIP, distIP=distIP, communicationCunt=count)
    # user_list = models.IOTTest.objects.all()
    field_list = store.get_fields()
    return render(request, "iot.html", {"data": field_list})
