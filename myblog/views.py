
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView  # DetailView
from .models import *
from .forms import *
from django.views import View

# Create your views here.

# all_posts = [

# ]


class StartingPageView(ListView):
    template_name = "myblog/home.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "myblog/posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(View):
    # template_name="myblog/post_detail.html"
    # model=Post
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {

            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)

        }
        return render(request, "myblog/post_detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        # else:

        context = {

            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "myblog/post_detail.html", context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:

            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "myblog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)

        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"]=self.object.tags.all()
    #     context["comment_form"]= CommentForm()
    #     return context


# def home(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3] #gives me the descending order, the latest post added on top

#     title = "My Blog"
#     context = {

#         "title": title,
#         "posts": latest_posts
#     }

#     return render(request, "myblog/home.html", context)


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     title = "All My Posts"
#     context = {

#         "title": title,
#         "all_posts":all_posts
#     }
#     return render(request, "myblog/posts.html", context)


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     context = {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     }
#     return render(request, "myblog/post-detail.html",  context)


# def get_date(post):
#     return post['date']
# sorted_posts = sorted(all_posts,key=get_date)
    # latest_posts =sorted_posts[-3:]

#  identified_post = next(post for post in all_posts if post['slug'] == slug)


# def post_detail(request, slug):
#     title = "All My Posts"
#     identified_post=next(post for post in all_posts if post['slug']==slug)
#     context = {
#         "post": identified_post
#     }
#     return render(request, "myblog/post_detail.html", context)
