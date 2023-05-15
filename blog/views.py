from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.http import require_POST


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)  # Form for users to comment
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 'comments':comments, 'form':form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleaned_data['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url} {cleaned_data['name']} comments: {cleaned_data['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cleaned_data['to']])
            sent = True
        else:
            form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent':sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',
                              {'post': post,
                               'form': form,
                               'comment': comment})