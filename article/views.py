from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm, AddressForm
from django.contrib import messages
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html")

def money(request):
    form = AddressForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        address = form.cleaned_data.get("city")
        messages.success(request,"{} li istifadeci burada yashayir {}".format(email, address))
        return redirect("index")
    return render(request, "money.html", {"form":form})

def articles(request):
    keyword = request.GET.get("keyword")
    choosenuser = request.GET.get("choosenuser")
    
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        if articles:
            return render(request, "articles.html", {"articles":articles})
        else:
            articles = Article.objects.filter(content__contains = keyword)
            return render(request, "articles.html", {"articles":articles}) 

    if choosenuser:
        articles = Article.objects.filter(author__contains = choosenuser)
        if articles:
            return render(request, "articles.html", {"articles":articles})            

    articles = Article.objects.all()
    return render(request, "articles.html", {"articles":articles})


def about(request):
    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    return render(request, "dashboard.html", {"articles":articles})

@login_required(login_url = "user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save() 
        messages.success(request, "Meqale elave olundu")
        return redirect("index")
    return render(request, "addarticle.html", {"form":form})

def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    
    return render(request, "detail.html", {"article":article, "comments":comments})

@login_required
def addComment(request,id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))


@login_required(login_url = "user:login")
def update(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Meqale yenilendi")
        return redirect("article:dashboard")
    return render(request, "update.html", {"form":form})

@login_required(login_url = "user:login")
def delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Meqale sikdirdi")
    return redirect("article:dashboard")