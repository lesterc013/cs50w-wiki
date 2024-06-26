from turtle import title
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse
import random
from django import forms

from . import util # From the same directory (aka encyclopedia) import the util module so we can use the functions defined within it

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    print("Entry Function")
    if title.lower() in util.lowercase_title_list():
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
        if query in util.lowercase_title_list():
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

def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        md_content = request.POST.get("content")
        # Need to add this encode() else everytime we get the content, the markdown file's spaces will be doubled
        encoded_content = md_content.encode()
        # Check if the title already exists
        if title.lower() in util.lowercase_title_list():
            # Return some rendering with the error message
            return render(request, "encyclopedia/newpage.html", {
                "title": "duplicate"
            })
        util.save_entry(title, encoded_content)
        # After the file is saved, the list however is not updated. Therefore when we use reverse, Django can't find the title to route the user. Fixed with making a method to lower case the title list automatically
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    return render(request, "encyclopedia/newpage.html")

class EditPageForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)

def editpage(request):
    if request.method == "GET":
        print(type(request))
        title = request.GET.get("title")
        content = util.get_entry(title)
        editPageForm = EditPageForm(initial={"content": content})
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "form": editPageForm
        })
    else:
        editPageForm = EditPageForm(request.POST)
        if editPageForm.is_valid():
            title = request.POST.get("title")
            print(title)
            content = editPageForm.cleaned_data["content"].encode()
            print(content)
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))


# def editpage(request):
#     if request.method == "GET":
#         title = request.GET.get("title")
#         print(title)
#         md_content = util.get_entry(title)
#         return render(request, "encyclopedia/editpage.html", {
#             "title": title,
#             "content": md_content
#         })
#     else:
#         title = request.POST.get("title")
#         md_content = request.POST.get("content")
#         encoded_content = md_content.encode()
#         util.save_entry(title, encoded_content)
#         return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

def randompage(request):
    title_list = util.list_entries();
    # Get a random int from 0 to len(title_list) - 1 cos that is the last index
    randInt = random.randint(0, len(title_list)-1)
    # Return the title of that random int index
    rand_title = title_list[randInt]
    return HttpResponseRedirect(reverse("entry", kwargs={"title": rand_title}))