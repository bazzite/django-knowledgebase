from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from .forms import CategoryForm
from .models import Category
from ..article.models import Article


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories_list'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        # Add in a QuerySet of the Articles
        context['articles'] = Article.objects.filter(
            category=self.object
        ).all().published()

        return context


class CategoryUpdateView(LoginRequiredMixin,
                         SuperuserRequiredMixin,
                         UpdateView):
    model = Category
    form_class = CategoryForm
    context_object_name = 'category'


class CategoryDeleteView(LoginRequiredMixin,
                         SuperuserRequiredMixin,
                         DeleteView):
    model = Category


class CategoryCreateView(LoginRequiredMixin,
                         SuperuserRequiredMixin,
                         CreateView):
    model = Category
    form_class = CategoryForm

    def form_valid(self, form):
        category = form.save(commit=False)

        category.author = self.request.user
        category.save()

        return super(CategoryCreateView, self).form_valid(form)
