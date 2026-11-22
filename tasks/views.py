from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView,TemplateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Task
from .forms import TaskForm
from categories.models import Category
# Create your views here.

# --list all tasks --
@login_required 
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    search_query = request.GET.get('search','')

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    context = {'tasks':tasks, 'search_query':search_query}
    return render(request, 'tasks/task_list.html', context)

# class TaskListView(LoginRequiredMixin,ListView):
#     model = Task
#     template_name ='tasks/task_list.html'
#     context_object_name = 'tasks'

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)
# ------------------------------------------------------------------
@login_required
def task_detail(request,pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    context = {'task':task}
    return render(request, 'tasks/task_detail.html', context)


# ------------------------------------------------------------------

# --- TASK CREATE ----

@login_required 
def task_create(request): 
    if request.method=='POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    context = {'form':form}
    return render(request , 'tasks/task_create.html', context)

# class TaskCreateView(LoginRequiredMixin,CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'tasks/task_create.html'
#     success_url = reverse_lazy('task_list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

# --------------------------------------------------------
# ---- TASK UPDATE ---
@login_required
def task_update(request,pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method=='POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    context = {'form':form}
    return render(request, 'tasks/task_update.html', context)

# class TaskUpdateView(UpdateView):
#     model = Task
#     form_class = TaskForm
#     success_url = reverse_lazy('task_list')
#     template_name = 'tasks/task_update.html'

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)
    
#     def get_form_kwargs(self):
#         kwargs= super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
# ------------------------------------------------------------

# --- TASK DELETE ---
@login_required
def task_delete(request,pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('task_list')

    context ={'task':task}
    return render(request, 'tasks/task_delete.html', context)

# class TaskDeleteView(LoginRequiredMixin,DeleteView):
#     model = Task
#     template_name = 'tasks/task_delete.html'
#     success_url = reverse_lazy('task_list')
#     pk_url_kwarg = 'pk'

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)
    

# ---------------------------------------------------------
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status=Task.Status.PENDING).count()
    in_progress_tasks = tasks.filter(status=Task.Status.IN_PROGRESS).count()
    completed_tasks = tasks.filter(status=Task.Status.COMPLETED).count()
    recent_tasks = tasks.order_by('-created_at')[:5]
    total_categories = Category.objects.filter(user=request.user).count()
    overdue_tasks = tasks.filter(due_date__lt=timezone.now()).exclude(status=Task.Status.COMPLETED)

    context = {
        'total_tasks':total_tasks,
        'pending_tasks':pending_tasks,
        'in_progress_tasks':in_progress_tasks,
        'completed_tasks':completed_tasks,
        'recent_tasks':recent_tasks,
        'total_categories':total_categories,
        'overdue_tasks': overdue_tasks,
        'overdue_count': overdue_tasks.count(),
    }

    return render(request, 'tasks/dashboard.html', context)

# class DashboardView(LoginRequiredMixin, TemplateView):
#     template_name = 'tasks/dashboard.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         tasks = Task.objects.filter(user=self.request.user)

#         context['total_tasks'] = tasks.count()

#         context['pending_tasks'] = tasks.filter(
#             status=Task.Status.PENDING
#         ).count()

#         context['in_progress_tasks'] = tasks.filter(
#             status=Task.Status.IN_PROGRESS
#         ).count()

#         context['completed_tasks'] = tasks.filter(
#             status=Task.Status.COMPLETED
#         ).count()

#         context['recent_tasks'] = tasks.order_by('-created_at')[:5]

#         context['total_categories'] = Category.objects.filter(
#             user=self.request.user
#         ).count()

#         return context