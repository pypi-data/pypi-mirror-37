# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import UserTrackRecord
from .forms import UserTrackRecordForm

User = get_user_model()


# Create your views here.
def test(request):
    return


# record

class RecordList(ListView):
    model = UserTrackRecord
    template_name = 'bee_django_track/user/record_list.html'
    context_object_name = 'record_list'
    paginate_by = 20

    def get_user(self):
        user_id = self.kwargs["user_id"]
        user = User.objects.get(id=user_id)
        return user

    def get_context_data(self, **kwargs):
        context = super(RecordList, self).get_context_data(**kwargs)
        context["user"] = self.get_user()
        return context

    def get_queryset(self):
        user = self.get_user()
        return UserTrackRecord.objects.filter(user=user)



class RecordDetail(DetailView):
    model = UserTrackRecord
    template_name = 'bee_django_track/user/record_detail.html'
    context_object_name = 'record'

    def get_context_data(self, **kwargs):
        context = super(RecordDetail, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        user = UserTrackRecord.objects.get(id=pk).user
        context["user"] = user
        return context


class RecordCreate(CreateView):
    model = UserTrackRecord
    form_class = UserTrackRecordForm
    template_name = 'bee_django_track/user/record_form.html'

    def form_valid(self, form):
        form.instance.user_id = self.kwargs["user_id"]
        form.instance.created_by = self.request.user
        return super(RecordCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bee_django_track:record_list', kwargs=self.kwargs)


class RecordUpdate(UpdateView):
    model = UserTrackRecord
    form_class = UserTrackRecordForm
    template_name = 'bee_django_track/user/record_form.html'

    def get_context_data(self, **kwargs):
        context = super(RecordUpdate, self).get_context_data(**kwargs)
        return context


class RecordDelete(DeleteView):
    model = UserTrackRecord
    success_url = reverse_lazy('bee_django_track:record_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)
