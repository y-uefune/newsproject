from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView,ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import NewsPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import NewsPost
from django.views.generic import DetailView
from django.views.generic import DeleteView


class IndexView(TemplateView):
    template_name = 'index.html'
    queryset = NewsPost.objects.order_by('-posted_at')
    paginate_by = 9

@method_decorator(login_required,name = 'dispatch')
class CreateNewsView(CreateView):
    form_class = NewsPostForm
    template_name = "post_news.html"
    success_url = reverse_lazy('news:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'


class CategoryView(ListView):
    template_name='index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = NewsPost.objects.filter(
            category=category_id
        ).order_by('-posted_at')
        return categories
    
class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = NewsPost.objects.filter(
            user=user_id
        ).order_by('-posted_at')
        return user_list
    
class DetailView(DetailView):
    template_name='detail.html'
    model = NewsPost

class MypageView(ListView):
    template_name='mypage.html'
    paginate_by = 9
    def get_queryset(self):
        queryset = NewsPost.objects.filter(
            user=self.request.user
        ).order_by('-posted_at')
        return queryset
    
class NewsDeleteView(DeleteView):
    model=NewsPost
    template_name='news_delete.html'
    success_url=reverse_lazy('news:mypage')

    def delete(self,request,*args,**kwargs):
        return super().delete(request,*args,**kwargs)