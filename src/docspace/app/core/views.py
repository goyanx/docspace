from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
import pandas as pd
import threading
from .models import *
from .utils import *


def index_view(request):
    return render(request, 'core/index.html', {
    })


@login_required
def upload_view(request):
    if 'upload_file' in request.FILES:
        doc = dict(
            name=request.FILES['upload_file'].name,
            pdf=request.FILES['upload_file'],
        )
        doc['upload_by'] = request.user
        doc = Document(**doc)
        doc.save()
        doc.process()
        threading.Thread(target=doc.update_chunks).start()
        return redirect('core:doc', doc_id=doc.id)
    return render(request, 'core/upload.html', {
    })


def about_view(request):
    return redirect('core:index')


@login_required
def docs_view(request):
    if request.user.username == 'nathan':
        docs = Document.objects.all()
    else:
        docs = Document.objects.filter(upload_by=request.user)

    if 'delete' in request.POST:
        doc = Document.objects.get(id=request.POST['delete'])
        try:
            doc.pdf.delete()
        except:
            pass
        doc.delete()

    if 'rename' in request.POST:
        doc = Document.objects.get(id=request.POST['rename'])
        doc.name = request.POST['new_name']
        doc.save()

    if 'download' in request.POST:
        doc = Document.objects.get(id=request.POST['download'])
        name = doc.name
        if not name.lower().endswith('.pdf'):
            name += '.pdf'
        return download_file(request, doc.pdf.file, name, content_type='application/pdf')
    
    if docs.count() == 0:
        return redirect('core:upload')

    return render(request, 'core/docs.html', {
        'docs': docs,
    })


@login_required
def doc_view(request, doc_id):
    doc = Document.objects.get(id=doc_id)
    if request.user != doc.upload_by:
        return HttpResponseForbidden()
    return render(request, 'core/doc.html', {
        'doc': doc,
    })


def login_view(request):
    if request.POST:
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('core:index')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:index')

