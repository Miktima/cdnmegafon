from django.shortcuts import render
from .forms import LogForm
import pandas as pd
from io import BytesIO
import base64
from django.contrib import messages
from zipfile import ZipFile

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


def index(request):
    form = LogForm()
    return render(request, "log_analize/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        if form.is_valid():
            filename = (request.FILES['file']).name
            ext_file = filename[(filename.rfind(".")+1):len(filename)]
            if ext_file == "csv":
                log_table = pd.read_csv(request.FILES['file'], sep=";")
            elif ext_file == "zip":
                archive = ZipFile(request.FILES['file'], 'r')
                filename_csv = (request.FILES['file'].name).replace(".zip", ".csv")
                log_table = pd.read_csv(archive.extract(filename_csv), sep=";")
            x=[]
            xticks = []
            for i in range(1,21):
                x.append(i)
                if (i%4) == 0:
                    xticks.append(i)
            # request_uri chart
            request_uri_ser = (log_table["request_uri"].value_counts()).head(20)
            request_uri_links = request_uri_ser.to_dict()
            request_uri_values = request_uri_ser.tolist()
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.bar(x, request_uri_values, width=1, edgecolor="white", linewidth=0.7, align='edge')
            ax.set(xlim=(1, 20), xticks=xticks)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            # fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
            # ax.plot(request_uri_values)
            # ax.set_xlabel('Номер позиции')
            ax.set_title("request_uri") 
            request_uri_img = BytesIO()
            plt.savefig(request_uri_img, format="png")
            request_uri_pic = base64.b64encode(request_uri_img.getvalue()).decode()
            plt.clf()
            # http_user_agent chart
            http_user_agent_ser = (log_table["http_user_agent"].value_counts()).head(20)
            http_user_agent_links = http_user_agent_ser.to_dict()
            http_user_agent_values = http_user_agent_ser.tolist()
            fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
            ax.bar(x, http_user_agent_values, width=1, edgecolor="white", linewidth=0.7, align='edge')
            ax.set(xlim=(1, 20), xticks=xticks)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_title("http_user_agent") 
            http_user_agent_img = BytesIO()
            plt.savefig(http_user_agent_img, format="png")
            http_user_agent_pic = base64.b64encode(http_user_agent_img.getvalue()).decode()
            plt.clf()
            # http_referer chart
            http_referer_ser = (log_table["http_referer"].value_counts()).head(20)
            http_referer_links = http_referer_ser.to_dict()
            http_referer_values = http_referer_ser.tolist()
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.bar(x, http_referer_values, width=1, edgecolor="white", linewidth=0.7, align='edge')
            ax.set(xlim=(1, 20), xticks=xticks)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_title("http_referer") 
            http_referer_img = BytesIO()
            plt.savefig(http_referer_img, format="png")
            http_referer_pic = base64.b64encode(http_referer_img.getvalue()).decode()
            plt.clf()
            # request_uri with 404 error 
            error404 = log_table.loc[log_table["status"] == 404, "request_uri"]
            error404_ser = (error404.value_counts()).head(20)
            error404_links = error404_ser.to_dict()
            error404_values = error404_ser.tolist()
            # Если размер списка меньше 20, дополняем нулями
            if error404_ser.size < 20:
                for i in range(error404_ser.size, 20):
                    error404_values.append(0)                   
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.bar(x, error404_values, width=1, edgecolor="white", linewidth=0.7, align='edge')
            ax.set(xlim=(1, 20), xticks=xticks)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_title("request_uri - error 404") 
            error404_img = BytesIO()
            plt.savefig(error404_img, format="png")
            error404_pic = base64.b64encode(error404_img.getvalue()).decode()
            plt.clf()
            context = {
                "request_uri_plot": request_uri_pic,
                "request_uri_links": request_uri_links,
                "request_uri_values": request_uri_values,
                "http_user_agent_plot": http_user_agent_pic,
                "http_user_agent_links": http_user_agent_links,
                "http_user_agent_values": http_user_agent_values,
                "http_referer_plot": http_referer_pic,
                "http_referer_links": http_referer_links,
                "http_referer_values": http_referer_values,
                "error404_plot": error404_pic,
                "error404_links": error404_links,
                "error404_values": error404_values,
                "filename": filename,
            }
            return render(request, "log_analize/results.html", context)
        else:
            form = LogForm()
            messages.error(request, form.errors)
            return render(request, "log_analize/index.html", {'form': form})            
    else:
        form = LogForm()
        return render(request, "log_analize/index.html", {'form': form})

