from turtle import title
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse

from . import util # From the same directory (aka encyclopedia) import the util module so we can use the functions defined within it

# Global title_list since multiple functions will need to use this
title_list_lowered = [x.lower() for x in util.list_entries()]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title.lower() in title_list_lowered:
        entry = markdown2.markdown(util.get_entry(title)) # Gets the entry related to the title and converts from markdown to HTML
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/invalid_entry.html", {
            "title": "Invalid Entry",
        })
    
def search(request):
    if request.method == "GET":
        query = request.GET.get('q').lower()
        if query in title_list_lowered:
            return HttpResponseRedirect(reverse("entry", kwargs={"title":query}))
        else:
            sub_list = []
            for title in util.list_entries():
                if query in title.lower():
                    sub_list.append(title) # title is in its original casing
            return render(request, "encyclopedia/search.html", {
                "sub_list": sub_list
            })
    return render(request, "encyclopedia/index.html")
        