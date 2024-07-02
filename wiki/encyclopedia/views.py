from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms


def index(request):
    if request.method == "POST":
        search = request.POST['q']
        search = str(search).strip()
        if util.get_entry(search) != None:
            return HttpResponse(util.get_entry(search))
        else:
            results = set()
            for i in util.list_entries():
                if str(search).upper() in str(i).upper():
                    results.add(i)
               
            return render(request, "encyclopedia/results.html",
                          {"results":results,"search":search})
        
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title_(request,title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/NotFound.html", {"name":title})
    else:
        return HttpResponse(util.get_entry(title))
    
def entry(request):
    if request.method == "POST":
        page = request.POST['wiki']
        page = str(page).strip()
        heading = request.POST['heading']
        heading = str(heading).strip()
        for k in util.list_entries():
            if heading.upper() == k.upper():
                return HttpResponse("Error Entry Title Already Exists")
            else:
                if 'submit' in request.POST:
                    return HttpResponse("WHOOOO")
        else:
            # request.session['page'] = page
            return render(request, "encyclopedia/entry.html", {
                "page": page,"heading":heading
            })
    return render(request, "encyclopedia/entry.html")
