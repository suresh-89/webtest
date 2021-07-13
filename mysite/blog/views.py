from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth import login, authenticate

from taggit.models import Tag
from .models import Post, Comment
from .forms import *


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('blog:mysite_login')
    else:
        form = SignUpForm()
    return render(request, 'blog/post/signup.html', {'form': form})

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        #Returns the result of filter() on a given model manager cast to a list, raising Http404 if the resulting list is empty.
        tag = get_object_or_404(Tag, slug=tag_slug)
        print("tags:", tag,type(tag))
        object_list = object_list.filter(tags__in=[tag])

    #a list of objects, plus the number of items you’d like to have on each page
    paginator = Paginator(object_list, 5) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    print("page {} posts {} posts type tag {}".format(page,posts,type(posts),tag))
    for x in posts:
        print("test",x,type(x))
    print("in console:",request.user)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    print('test',post,year,month,day)
    print('test1',Post.objects.filter(slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   # publish__day=day
                                   ))
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   # publish__month=month,
                                   # publish__day=day
                                   )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})






def post_search(request):
    form = SearchForm()
    print("jasvyjew",request.method)
    if request.method == 'POST':
    #if 'query' in request.GET:
        form = SearchForm(request.POST)
        print("test",form.is_valid())
        if form.is_valid():
            search_text = form.cleaned_data['query']
            results = Post.objects.filter(title__contains=search_text)
            cd = form.cleaned_data
            # results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            # # count total results
            total_results = results.count()
            return render(request, 'blog/post/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results})
    else:
        form = SearchForm()
        return render(request, 'blog/post/search.html', {'form': form,
                                                         })



