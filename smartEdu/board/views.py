import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt

from .models import Board,Comment

# Create your views here.
def board(request):
    boardCount = Board.objects.count()
    boardList = Board.objects.all().order_by("-idx")
    return render(request, "board.html", {"boardList" : boardList, "boardCount" : boardCount})

def write(request):
    return render(request,"write.html")

UPLOAD_DIR = ' / up / '

@csrf_exempt
def insert(request):
    fname = ""
    fsize = 0
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file.name
        fsize = file.size
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto = Board(writer=request.POST["writer"], title=request.POST["title"], content=request.POST["content"],
                filename=fname, filesize=fsize)
    dto.save()
    print(dto)
    return redirect("/board")

def download(request):
    id = request.GET['idx']
    dto = Board.objects.get(idx = id)
    path = UPLOAD_DIR + dto.filename
    filename = os.path.basename(path)
    filename = filename.encode('utf-8')
    filename = urlquote(filename)
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type = "application/octet-stream")
        response["Content-Disposition"] = "attachment; filename* = UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save()
        return response


def detail(request):
    id = request.GET["idx"]
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()

    print("filesize : ", dto.filesize)
    filesize = "%.2f" % (dto.filesize / 1024)
    return render(request, "detail.html", {"dto": dto, "filesize": filesize, })


@csrf_exempt
def update(request):
    id = request.POST['idx']
    dto_src = Board.objects.get(idx=id)
    fname = dto_src.filename
    fsize = 0
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file.name
        # fsize = file.size
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        fsize = os.path.getsize(UPLOAD_DIR + fname)

    dto_new = Board(idx=id, writer=request.POST["writer"], title=request.POST["title"], content=request.POST["content"],
                    filename=fname, filesize=fsize)
    dto_new.save()
    return redirect("/board")

@csrf_exempt
def delete(request):
    id = request.POST['idx']
    Board.objects.get(idx = id).delete()
    return redirect("/board")

@csrf_exempt
def reply_insert(request):
    id = request.POST['idx']
    dto = Comment(board_idx=id, writer=request.POST["writer"], content=request.POST["content"])
    dto.save()
    return HttpResponseRedirect("detail?idx="+id)
















