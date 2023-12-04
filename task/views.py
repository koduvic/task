from django.shortcuts import render, redirect
from . models import Task
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth.mixins import LoginRequiredMixin
from  django.contrib.auth.decorators import login_required

# Create your views here.

# Login view
class CustomLogin(LoginView):
    template_name='task/login.html'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('index')
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(CustomLogin, self).get(*args, **kwargs)



#Register Page

class RegisterPage(FormView):
    template_name='task/register.html' 
    form_class=UserCreationForm
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
        
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(*args, **kwargs)
def index(request):
    return render(request, 'task/index.html')

@login_required(login_url='login')
def tasks(request):
    q=request.GET.get('q') or ''
    user_id=request.user.id
    myTasks=Task.objects.filter(user=user_id)
    if (q):
        tasks=myTasks.filter(title__icontains=q)
    else:

        tasks=myTasks
    
    
    return render(request, 'task/tasks.html', {'tasks':tasks })

@login_required(login_url='login')
def task_details(request, pk):
    task=Task.objects.get(id=pk)
    return render(request, 'task/task_details.html', {'task':task})

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    fields=['title', 'description', 'complete']
  
    success_url=reverse_lazy('tasks')
    template_name='task/task_form.html'
    def form_valid(self, form):
         form.instance.user=self.request.user
         return super(TaskUpdate, self).form_valid(form)

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title', 'description', 'complete']
  
    success_url=reverse_lazy('tasks')
    template_name='task/task_form.html'
    def form_valid(self, form):
         form.instance.user=self.request.user
         return super(TaskCreate, self).form_valid(form)




class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
    template_name='task/task_delete.html'