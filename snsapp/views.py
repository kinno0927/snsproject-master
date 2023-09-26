from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Tag
from .models import Post 
from .forms import PostForm

from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.shortcuts import render
from .forms import SignupForm  # アカウント作成フォームのインポート

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合の処理（新しいユーザーを作成など）
            pass
    else:
        form = SignupForm()

    context = {'form': form}

    # フォームが無効な場合、エラーメッセージを追加
    if form.errors:
        context['errors'] = form.errors

    return render(request, 'signup.html', context)



class TagListView(LoginRequiredMixin,ListView):
    """タグ一覧"""
    model = Tag
    template_name = 'tag.html'
    context_object_name = 'tags'         
    
class SearchTagView(View):
    template_name = 'search_tag.html'

    def get(self, request, *args, **kwargs):
        tag_name = request.GET.get('tag_name')  # URLパラメータからタグ名を取得
        if tag_name:
            tags = Tag.objects.filter(name__icontains=tag_name)  # タグ名の部分一致検索
        else:
            tags = Tag.objects.none()  # タグ名が指定されていない場合は空のQuerySet

        context = {'tags': tags, 'searched_tag_name': tag_name}
        return render(request, self.template_name, context)

class CreateTag(LoginRequiredMixin, CreateView):
    """投稿フォーム"""
    model = Tag
    template_name = 'create_tag.html'
    fields = ['name']
    success_url = reverse_lazy('tag')



class Home(LoginRequiredMixin, ListView, CreateView):
    """HOMEページで、自分以外のユーザー投稿をリスト表示"""
    model = Post
    form_class = PostForm
    template_name = 'list.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('home-tag')    
    paginate_by = 1000

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name', None)
        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tag_name'] = self.kwargs.get('tag_name', None)
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            post = form.save(commit=False)
            tag_name = self.kwargs.get('tag_name', None)
            tag, created = Tag.objects.get_or_create(name=tag_name)  # タグを取得または作成
            post.tag = tag
            post.user = self.request.user
            post.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        """投稿ユーザーをリクエストユーザーと紐付けて保存"""
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        tag_name = self.kwargs.get('tag_name')  # 現在のページのtag_nameを取得
        return reverse_lazy('home-tag', kwargs={'tag_name': tag_name})
        
        
class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    


class CreatePost(LoginRequiredMixin, CreateView):
    """投稿フォーム"""
    model = Post
    template_name = 'create.html'
    fields = ['content','tag']
    success_url = reverse_lazy('tag')

    def form_valid(self, form):
        """投稿ユーザーをリクエストユーザーと紐付け"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailPost(LoginRequiredMixin, DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """投稿編集ページ"""
    model = Post
    template_name = 'update.html'
    fields = ['title', 'content']


    def get_success_url(self,  **kwargs):
        """編集完了後の遷移先"""
        pk = self.kwargs["pk"]
        return reverse_lazy('detail', kwargs={"pk": pk})
    
    def test_func(self, **kwargs):
        """アクセスできるユーザーを制限"""
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user) 


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """投稿編集ページ"""
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('mypost')

    def test_func(self, **kwargs):
        """アクセスできるユーザーを制限"""
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user) 


###############################################################
#いいね処理
class LikeBase(LoginRequiredMixin, View):
    """いいねのベース。リダイレクト先を以降で継承先で設定"""
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)

        if self.request.user in related_post.like.all():
            obj = related_post.like.remove(self.request.user)
        else:
            obj = related_post.like.add(self.request.user)  
        return obj


class LikeHome(LikeBase):
    """HOMEページでいいねした場合"""
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('home-tag')


class LikeDetail(LikeBase):
    """詳細ページでいいねした場合"""
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('detail', pk) 
    
###############################################################



