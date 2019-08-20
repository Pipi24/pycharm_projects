import shutil
import time

from django.shortcuts import render

from rg import crud
from rg.preprocess import cnn_predict
from rg.preprocess import pcap2sess
from rg.preprocess import process_sess
from rg.preprocess import sess2field
from rg.preprocess import sess2input
from rg.reverse_resolve import ip_host

IS_CLASSIFY_TRAFFIC = False
dict_6class_novpn = {0: 'Chat', 1: 'Email', 2: 'File Transfer',
                     3: 'P2P', 4: 'Streaming', 5: 'VoIP'}


# Create your views here.
def upload_pcap(request):
    start = time.time()
    if request.method == 'POST':
        try:
            path = request.POST.get('file_path', None)
            # path = '/home/wuhiu/deeplearning/VPNData/non-vpn/Chat/AIMchat1.pcap'

            # get ip and host map
            dict_ip_host = ip_host.get_ip_host(path)
            split_dir = pcap2sess.split_pcap(path)
            # pcap2sess.filter_lack_pcap(split_dir)
            unify_dir = process_sess.unify_sess(split_dir)
            list_fields = sess2field.get_field(unify_dir)

            # get fields and communication way from pcap
            if IS_CLASSIFY_TRAFFIC:
                x_pred = sess2input.get_cnn_input(unify_dir)
                preds = cnn_predict.predict(x_pred)
                print('preds: ', preds)
                for i, fields in enumerate(list_fields):
                    fields['comm_way'] = dict_6class_novpn[preds[i]]
            print('list_fields: ', list_fields)
        except:
            shutil.rmtree(split_dir)
            shutil.rmtree(unify_dir)
        else:
            shutil.rmtree(split_dir)
            shutil.rmtree(unify_dir)
            crud.insert_relations(dict_ip_host, list_fields)
            # crud.insert_ip_host(dict_ip_host)
            # crud.insert_fields(list_fields)
            # crud.join_fields_host()

    list_rgs = crud.query_rg_v2()
    end = time.time()
    print('query time: ', str(end - start))
    return render(request, "upload.html", {'list_rgs': list_rgs})


def get_rgs(request):
    pass
