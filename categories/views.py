from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category
from .forms import CategoryForm

# Create your views here.

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    context = {'categories':categories}
    return render(request , 'categories/category_list.html', context)

# class CategoryListView(LoginRequiredMixin,ListView):
#     model = Category
#     template_name = 'categories/category_list.html'
#     context_object_name = 'categories'
#     def get_queryset(self):
#         categories = Category.objects.filter(user=self.request.user)
#         return categories

# ---------------------------------------
@login_required
def category_create(request):
    if request.method=='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    context ={'form':form}
    return render(request, 'categories/category_create.html' , context)

# class CategoryCreateView(LoginRequiredMixin,CreateView):
#     model= Category
#     form_class = CategoryForm
#     template_name = 'categories/category_create.html'
#     success_url = reverse_lazy('category_list')

#     def form_valid(self, form):
#         form.instance.user=self.request.user
#         return super().form_valid(form)
    
# ---------------------------------------------------

# Category Update
@login_required
def category_update(request,pk):
    category = get_object_or_404(Category,pk=pk,user=request.user)
    if request.method=='POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    context ={'form':form}
    return render(request, 'categories/category_update.html' , context)

# class CategoryUpdateView(LoginRequiredMixin,UpdateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'categories/category_update.html'
#     pk_url_kwarg ='pk'
#     success_url = reverse_lazy('category_list')

#     def get_queryset(self):
#         category = Category.objects.filter(user=self.request.user)
#         return category
    
# ------------------------------------------

# -- Delete Category
@login_required
def category_delete(request,pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method=='POST':
            category.delete()
            return redirect('category_list')
    context = {'category': category}
    return render(request, 'categories/category_delete.html', context)

# class CategoryDeleteView(LoginRequiredMixin,DeleteView):
#     model = Category
#     template_name = 'categories/category_delete.html'
#     pk_url_kwarg = 'pk'
#     success_url = reverse_lazy('category_list')

#     def get_queryset(self):
#         return Category.objects.filter(user=self.request.user)