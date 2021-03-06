from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, Comment, Reuniao
from .forms import PostForm, CommentForm, ContatoForm, ReuniaoForm, CommentFormSet

# import pdb

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_tag_list(request, pk):
    posts = Post.objects.filter(tags__id=pk)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    post.visits += 1
    post.save()

    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def new_post(request):
    if not request.user.is_authenticated():
       # raise Http404
       return HttpResponseNotFound('<h1>404 - Not found :(</h1>')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            # forcing to save the m2m attributte 'cause of commit=False
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(initial={'title': 'Título aqui...'})
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # update the instance
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            # forcing to save the m2m attributte 'cause of commit=False
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    # Post.objects.filter(pk=pk).delete()
    post = get_object_or_404(Post, pk=pk)
    post.delete()

    return redirect('post_list')

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        formset = CommentFormSet(request.POST)
        if formset.is_valid():
            for form in formset.forms:
                comment = form.save(commit=False)
                if request.user.is_authenticated():
                    comment.author = request.user.username
                comment.post = post
                comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        formset = CommentFormSet()

        return render(request, 'blog/add_comment_to_post.html', {'formset': formset})


# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             if request.user.is_authenticated():
#                 comment.author = request.user.username
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#         return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def contato(request):
    if request.method == 'GET':
        email_form = ContatoForm()
    else:
        email_form = ContatoForm(request.POST)
        if email_form.is_valid():
            emissor = email_form.cleaned_data['emissor']
            assunto = email_form.cleaned_data['assunto']
            msg = email_form.cleaned_data['msg']

            try:
                send_mail(assunto, msg, emissor, ['alexandreabreu@comp.ufla.br'])
            except BadHeaderError:
                return HttpResponse("Erro =/")
            return redirect('obg')
    return render(request, 'blog/email.html', {'form': email_form})

def obg(request):
    return HttpResponse("<h2>Obrigado pela mensagem!!!</h2>")

def reunioes(request):
    reunioes = Reuniao.objects.all()
    return render(request, 'blog/reunioes_list.html', {'reunioes': reunioes})

def reuniao_presenca(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    if request.method == "POST":
        # update the instance
        form = ReuniaoForm(request.POST, instance=reuniao)
        if form.is_valid():
            reuniao = form.save(commit=False)
            reuniao.save()
            # forcing to save the m2m attributte 'cause of commit=False
            form.save_m2m()
            return redirect('reunioes')
    else:
        form = ReuniaoForm(instance=reuniao)
    return render(request, 'blog/reuniao_edit.html', {'form': form})


def ajax(request):
    return render(request, 'blog/ajax.html', {})

def get_qtd_posts(request):
    pass

def get_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post_json = {
            'status': 1,
            'id': post.id,
            'author': str(post.author),
            'title': post.title,
            'visits': post.visits,
            'text': post.text
        }
    except ObjectDoesNotExist:
        post_json = {'status': 0}
    return JsonResponse(post_json)

def ajax_post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        post_json = {'status': 1}
    except ObjectDoesNotExist:
        post_json = {'status': 0}
    return JsonResponse(post_json)