from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

class OwnerRequiredMixin(LoginRequiredMixin):

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.assigned_to != self.request.user:
            raise Http404("У вас немає доступу до цієї задачі.")
        return obj
