#  Description: Music Monolith Marketing Website
#  Author: Benjamin Orrvick
#  Author URL:  https://github.com/borrvick/
#  Purpose: create the user aspect of website mainly account CRUD
#  Tags: Music, Marketing, Business, Website, Application


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView
from spotify.models import CSVFile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == "POST":
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            messages.success(
                request, "Your account has been created! You can now log in."
            )
            return redirect("login")
    else:
        # all other forms that arent a post request
        u_form = UserRegisterForm()
        context = {"title": "Update Account", "u_form": u_form}
    return render(request, "users/register.html", context)


# displays the csv files in the recent searches part of profile(most recent 5)
class CSVListView(LoginRequiredMixin, ListView):
    model = CSVFile
    template_name = "users/history.html"
    context_object_name = "csvs"

    def get_queryset(self):
        return CSVFile.objects.filter(profile=self.request.user.profile)


@login_required
def profileUpdate(request):

    if request.method == "POST":

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            "title": "Update Account",
            "u_form": u_form,
            "p_form": p_form,
        }

    return render(request, "users/profile_update.html", context)


@login_required
def profile(request):

    return render(request, "users/profile.html", {"title": "Account"})


@login_required
def profileConfirmDelete(request, pk):

    try:

        # makes sure if user is deleted that ass associated seaches are deleted as well
        for x in CSVFile.objects.filter(profile=request.user.profile):
            x.delete()
        # make sure the active user is the one getting deleted from db
        u = User.objects.get(pk=pk)
        u.delete()
        messages.success(request, "The user was deleted")
    except User.DoesNotExist:
        messages.error(request, "The User does not exist")
        return render(request, "users/profile.html")

    except Exception as e:
        return render(request, "users/profile.html", {"err": e.message})

    return render(request, "users/post_profile_delete.html")


@login_required
def profileDelete(request):
    return render(
        request,
        "users/profile_confirm_delete.html",
        {"title": "Delete Account"},
    )


def postProfileDelete(request):
    return render(request, "users/register.html")
