from django.shortcuts import render

from . import util
from markdown2 import Markdown
import random

def convert_md(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        search = request.POST['q']
        html_content = convert_md(search)
        if html_content:
                return render(request, "encyclopedia/entry.html", {
                "title": search,
                "content": html_content
                })
        else:
            allEntries = util.list_entries()
            recommendations =[]
            for entry in allEntries:
                if search.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendations": recommendations
            })

def createnewpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/createnewpage.html") 
    else:
        title = request.POST['title']
        content= request.POST['content']

        if title =='' or content =='':
            return render(request,"encyclopedia/error.html", {
                "message": "Title and content cannot be empty"
            })

        checkTitle = util.get_entry(title)

        if checkTitle:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
        if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']

            if title =='' or content =='':
                return render(request,"encyclopedia/error.html", {
                "message": "Title and content cannot be empty"
            })
            
            util.save_entry(title, content)
            html_content = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })


def rand(request):
    allEntries = util.list_entries()
    rand = random.choice(allEntries)
    html_content = convert_md(rand)
    return render(request, "encyclopedia/entry.html", {
        "title": rand,
        "content": html_content
    })