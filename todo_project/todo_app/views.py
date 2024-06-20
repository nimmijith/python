from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from todo_app.forms import TodoForm
from todo_app.models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView


# Create your views here.

class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'


class TaskDetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'


class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('taskname', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})


class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


def index(request):
    return render(request, 'home.html')


def add(request):
    if request.method == 'POST':
        taskname = request.POST.get('taskname', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        task = Task(taskname=taskname, priority=priority, date=date)
        task.save()

    task1 = Task.objects.all()

    return render(request, 'home.html', {'task1': task1})


# def detail(request):
#     task1 = Task.objects.all()
#
#     return render(request, 'detail.html', {'task1': task1})


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == "POST":
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')


def update(request, Id):
    task = Task.objects.get(id=Id)
    f = TodoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request, 'edit.html', {'f': f, 'task': task})
