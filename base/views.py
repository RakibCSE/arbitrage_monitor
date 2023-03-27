from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.views import SignupView, LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CoinDetails, NewsDetails

import logging

LOG_FORMAT = "%(levelname)s >  Line:%(lineno)s - %(message)s"
logging.basicConfig(filename="test.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w",
                    )
logger = logging.getLogger(__name__)


class MyLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            pass
        return super(MyLoginView, self).dispatch(request, *args, **kwargs)

    template_name = "base_app/login.html"


class MySignupView(SignupView):
    # Signup form extended using MyCustomSignupForm
    form_class = MyCustomSignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            pass
            # return redirect('user_accounts:profile')
        return super(MySignupView, self).dispatch(request, *args, **kwargs)

    template_name = "base_app/signup.html"


def index(request):
    """
    index: Home page of the website
    :param request:
    :return HTML:
    :return CONTEXT:
    """
    try:
        news_details = NewsDetails.objects.all()
        top_heading_news = news_details[0]
        latest_news = news_details[1:]

        return render(request, "base_app/home.html", {
            'top_heading_news': top_heading_news,
            'latest_news': latest_news,
        })

    except Exception as err:
        logger.warning("Exception found in index view: {}".format(err))
        # Return homepage if exception is found
        return render(request, "base_app/home.html")


@login_required
def edit_profile(request):
    """
    edit_profile: Edit profile of the current user
    :param request:
    :return request:
    :return HTML:
    :return CONTEXT: Two forms
    """
    try:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect("base:profile", request.user.id)
            else:
                messages.error(request, 'Please check the connection.')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)

        return render(request, 'base_app/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
    except Exception as err:
        logger.warning("Exception in edit_profile view: {}".format(err))


@login_required()
def show_profile(request, id):
    """
    show_profile: Shows the profile of the current user who logged in
    :param request:
    :param id:
    :return request:
    :return HTML:
    :return CONTEXT:
    """
    try:
        user_object = User.objects.get(id=id)
        return render(request, "base_app/profile.html", {
            "user_object": user_object,
        })
    except Exception as err:
        logger.warning("Exception found in show_profile view: {}".format(err))


def about(request):
    """
    about: Shows about page of the webpage.
    :param request:
    :return request:
    :return HTML:
    """
    return render(request, 'base_app/about.html')


def show_all_cryptocurrencies(request):
    """
    show_all_cryptocurrencies: Shows all cryptocurrency exchanges
    :param request:
    :return request:
    :return HTML:
    :return CONTEXT VARIABLE:
    """
    try:
        coin_details_object = list(CoinDetails.objects.all())

        # For pagination on homepage
        page = request.GET.get('page', 1)
        paginator = Paginator(coin_details_object, 10)

        try:
            coin_data_page = paginator.page(page)
        except PageNotAnInteger:
            coin_data_page = paginator.page(1)
        except EmptyPage:
            coin_data_page = paginator.page(paginator.num_pages)
        return render(request, "base_app/cryptocurrencies.html", {
            "coin_data": coin_data_page,
        })
    except Exception as err:
        logger.warning("Exception found in show_all_cryptocurrencies: {}".format(err))
