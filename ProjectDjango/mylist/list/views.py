from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy 

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'list/login.html'
    field = '__all__'
    redirect_authenticated_user =True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name='list/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user =True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')  # ✅ Call redirect with the correct URL name
        return super().get(request, *args, **kwargs)  # ✅ Corrected 'get' method call

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        search_input = self.request.GET.get('search-area') or ''
        queryset = Task.objects.filter(user=self.request.user)

        if search_input:
            queryset = queryset.filter(title__icontains=search_input)  # ✅ Ensure filtering happens here #title__startswith for finding with a starting word

        return queryset  # ✅ Returning correctly filtered queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(complete=False).count()  
        context['search_input'] = self.request.GET.get('search-area') or ''  # ✅ Fixed variable name
        return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    template_name='list/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields =['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields =['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url = reverse_lazy('tasks')

