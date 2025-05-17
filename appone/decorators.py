# fitness/decorators.py
from django.http import Http404
from .models import Consultant

def consultant_required(function):
    def wrap(request, *args, **kwargs):
        try:
            consultant = request.user.consultant
        except Consultant.DoesNotExist:
            raise Http404("شما دسترسی به این بخش ندارید.")
        return function(request, *args, **kwargs)
    return wrap
