"""editdojo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from startpage.views import startpageView, startstateView, startparkView
from startpage.views import searchParks, searchParks2, setUpParkView

from parkpage.views import parkpageView

from parkpage.views import alertsView, visitorView, eventView, campgroundView, learnView
from parkpage.views import lessonView, newsView, articleView, peopleView, placeView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('start/', startpageView),
    path('startstate/', startstateView),
    path('startpark/', startparkView),

    path('searchParks/', searchParks),
    path('searchParks2/<str:search_term>/', searchParks2),
    path('setUpPark/<str:park_code>/', setUpParkView),

    path('park/<str:park_code>/', parkpageView),

    path('alerts/<str:park_code>/', alertsView),
    path('visitor/<str:park_code>/', visitorView),
    path('events/<str:park_code>/', eventView),
    path('campground/<str:park_code>/', campgroundView),
    path('learn/<str:park_code>/', learnView),

    path('lesson/<str:park_code>/', lessonView),
    path('news/<str:park_code>/', newsView),
    path('articles/<str:park_code>/', articleView),
    path('people/<str:park_code>/', peopleView),
    path('places/<str:park_code>/', placeView),


]

urlpatterns += staticfiles_urlpatterns()
