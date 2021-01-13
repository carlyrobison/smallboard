from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import RedirectView

from .forms import HuntForm
from .models import Hunt

import logging


logger = logging.getLogger(__name__)


@login_required(login_url="/")
def index(request):
    form = HuntForm()

    if request.method == "POST":
        form = HuntForm(request.POST)
        if form.is_valid():
            hunt = Hunt(
                name=form.cleaned_data["name"],
                url=form.cleaned_data["url"],
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
            )
            hunt.save()

    context = {
        "active_hunts": Hunt.objects.filter(active=True).order_by("-created_on"),
        "finished_hunts": Hunt.objects.filter(active=False).order_by("-created_on"),
        "form": form,
    }
    return render(request, "index.html", context)


@login_required(login_url="/")
def stats(request, hunt_slug):
    hunt = Hunt.get_object_or_404(user=request.user, slug=hunt_slug)

    num_solved = hunt.get_num_solved()
    num_unsolved = hunt.get_num_unsolved()
    num_unlocked = hunt.get_num_unlocked()
    num_metas_solved = hunt.get_num_metas_solved()
    solves_per_hour = hunt.get_solves_per_hour()
    minutes_per_solve = hunt.get_minutes_per_solve()

    context = {
        "num_solved": num_solved,
        "num_unsolved": num_unsolved,
        "num_unlocked": num_unlocked,
        "num_metas_solved": num_metas_solved,
        "solves_per_hour": solves_per_hour,
        "minutes_per_solve": minutes_per_solve,
        "hunt_name": hunt.name,
        "hunt_slug": hunt.slug,
    }

    return render(request, "stats.html", context=context)


@login_required(login_url="/")
def redirect_to_drive(request, hunt_slug):
    # TODO: make hunt specific
    if settings.GOOGLE_HUMAN_DRIVE_HUNT_FOLDER_URL:
        return HttpResponseRedirect(settings.GOOGLE_HUMAN_DRIVE_HUNT_FOLDER_URL)
    else:
        messages.error(
            request, f"Google API disabled. Cannot redirect to Google folder"
        )
        return redirect("/")


class LastAccessedHuntRedirectView(LoginRequiredMixin, RedirectView):
    login_url = "/"
    pattern_name = "hunts:all_puzzles_react"

    def get_redirect_url(self, *args, **kwargs):
        hunt = self.request.user.last_accessed_hunt
        if not hunt:
            return reverse("hunts:index")
        kwargs["hunt_slug"] = hunt.slug
        return super().get_redirect_url(*args, **kwargs)


class ReactHuntView(LoginRequiredMixin, View):
    login_url = "/"
    redirect_field_name = "next"

    def get(self, request, hunt_slug):
        hunt = Hunt.get_object_or_404(user=request.user, slug=hunt_slug)

        context = {
            "hunt_pk": hunt.pk,
        }
        return render(request, "all_puzzles_react.html", context)
