from django.contrib import admin
from django.utils import timezone
from .models import Candidate, Vote, ElectionControl


def is_results_allowed():
    control = ElectionControl.objects.first()

    if not control:
        return False

    # Voting still running
    if control.end_time and timezone.now() < control.end_time:
        return False

    # Results not declared
    if not control.show_results:
        return False

    return True


# 🔒 Vote Admin Lock
class VoteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if not is_results_allowed():
            return Vote.objects.none()
        return super().get_queryset(request)


# 🔒 Candidate Admin Lock (IMPORTANT 🔥)
class CandidateAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if not is_results_allowed():
            return Candidate.objects.all().annotate(votes_hidden=0)
        return super().get_queryset(request)


admin.site.register(Vote, VoteAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(ElectionControl)