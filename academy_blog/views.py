from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Article
from .froms import ArticleForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView



def user_is_staff(user):
    return user.is_staff


# Create your views here.
@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'create.html'
    success_url = reverse_lazy('article_view')


class ArticleListView(ListView):
    model = Article
    template_name = 'blog.html'
    context_object_name = 'articles'
    paginate_by = 12
    queryset = Article.objects.select_related('category')


    def get_queryset(self):
        query_set = super().get_queryset()
        where = []
        q = self.request.GET.get('q', None)
        cid = self.kwargs.get('id')
        
        if q:
            where.append(Q(title__icontains=q))
        if cid:
            where.append(Q(category_id=cid))

        if where:
            from functools import reduce
            from operator import or_

            query_set = query_set.filter(reduce(or_, where))

        return query_set
    

class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'art'
    template_name = 'single.html'

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'update.html'
    success_url = reverse_lazy('article_view')

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('article_view')
