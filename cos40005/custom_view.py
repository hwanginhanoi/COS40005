
from django.shortcuts import render
from django.views.generic import ListView

class SomeCustomView(ListView):
    admin = {}

    def get(self, request):
        ctx = self.admin.each_context(request)
        return render(request, 'admin/dataexport.html', ctx)
