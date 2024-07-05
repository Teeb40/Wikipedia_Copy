from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms
import random
import markdown2
def index(request):
    
    if request.method == "POST":
        search = request.POST['q']
        search = str(search).strip()
        if util.get_entry(search) != None:
            wiki = markdown2.markdown(util.get_entry(search))
            return render(request,"encyclopedia/pages.html",{"markdown_content":wiki,"link":search,
                                                         "entry_":random.choice(util.list_entries())})
        else:
            results = set()
            for i in util.list_entries():
                if str(search).upper() in str(i).upper():
                    results.add(i)
               
            return render(request, "encyclopedia/results.html",
                          {"results":results,
                           "search":search,
                           "entry_":random.choice(util.list_entries())})
        
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "entry_":random.choice(util.list_entries())
    })


def title_(request,title):
    
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/NotFound.html", 
                      {"name":title,"entry_":random.choice(util.list_entries())})
    else:
        wiki = markdown2.markdown(util.get_entry(title))
        return render(request,"encyclopedia/pages.html",{"markdown_content":wiki,"link":title,
                                                         "entry_":random.choice(util.list_entries())})
    
def entry(request):
    if request.method == "POST":
        page = request.POST['wiki']
        page = str(page).strip()
        heading = request.POST['heading']
        heading = str(heading).strip()
        for i in heading:
            if i == " ":
                i = ""
            list(heading).append(i)
        for k in util.list_entries():
            if heading.upper() == k.upper():
                return HttpResponse("Error Entry Title Already Exists")
            else:
                if len(page) != 0 and len(heading) != 0:
                    util.save_entry(heading,page)
                else:
                    return HttpResponse("Not a Sufficient Entry")
                if 'submit' in request.POST:
                    return HttpResponse("WHOOOO")
        else:
    
            if len(page) != 0 and len(heading) != 0:
                util.save_entry(heading,page)
            else:
                return HttpResponse("Not a Sufficient Entry")
            wiki = markdown2.markdown(util.get_entry(heading))
            return render(request,"encyclopedia/pages.html",{"markdown_content":wiki,"link":heading,
                                                             "entry_":random.choice(util.list_entries())})
            
    return render(request, "encyclopedia/entry.html", 
                  {"entry_":random.choice(util.list_entries())})


def edit(request,edit_page):
    content = util.get_entry(edit_page)
    entries = [x.lower() for x in util.list_entries()]
    if request.method == "POST":
        wiki = request.POST["wiki"]
        heading = request.POST["heading"]
        if str(heading).strip().lower() not in entries:
            return HttpResponse("Page Edited Did not contain the same title, Please Maintain the title Otherwise Make a New Entry")
        else: 
            util.save_entry(heading,wiki)
            markdown_content = markdown2.markdown(util.get_entry(heading))
            return render(request,"encyclopedia/pages.html",{"markdown_content":markdown_content,"link":heading,
                                                             "entry_":random.choice(util.list_entries())})
    if str(edit_page).lower() in entries:
        return render(request, "encyclopedia/change.html", 
                    {"edit_page":edit_page,
                    "content":content,
                    "entry_":random.choice(util.list_entries())})
    
            

    else:
        return HttpResponse("Page Not Found")