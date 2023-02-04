import random

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import About, Events, Department, Service, Visitor, News, Feedback, Resource
from datetime import date, datetime, timedelta
from random import sample
from django.db import models
from .forms import VisitorForm, EventForm, FeedbackForm, RegisterUserForm
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User


def home(request):
    events = [event for event in Events.objects.select_related('department').all() if event.date.timestamp() > datetime.now().timestamp()]
    news = News.objects.select_related('department').all().filter(publish='YES').order_by('-date')[:10]
    if request.user.is_authenticated:
        news = News.objects.select_related('department').all().exclude(publish='NO')
    services = Service.objects.all()
    departments = [i for i in Department.objects.all() if i.status == 'Active']
    resources = Resource.objects.all()
    return render(request, 'tisdac_app/index.html', {'events': events,
                                                     'news': news,
                                                     'services': services,
                                                     'departments': departments,
                                                     'resources': resources})

#Использую функцию выше home
class HomeView(TemplateView):
    template_name = 'tisdac_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = [event for event in Events.objects.select_related('department').all() if event.date.timestamp() > datetime.now().timestamp()]
        context['news'] = News.objects.select_related('department').all().order_by('-date')[:10]
        context['services'] = Service.objects.all()
        context['departments'] = [i for i in Department.objects.all() if i.status == 'Active']
        context['resources'] = Resource.objects.all()
        return context


def main(request):
    #context = {'main'=}

    return render(request, 'tisdac_app/index.html', )


def about(request):
    articles = About.objects.all()
    return render(request, 'tisdac_app/about.html', {'articles': articles})


class ContactView(FormView):
    form_class = FeedbackForm
    template_name = 'tisdac_app/contact.html'
    success_url = 'contact/done'

    def form_valid(self, form):
        feed = Feedback(
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            email=form.cleaned_data['email'],
            feedback=form.cleaned_data['feedback'],
            date=datetime.now(),
        )
        feed.save()

        #sending Email
        template_email = render_to_string('email/email_feedback.html', {'name': form.cleaned_data['name'],
                                          'feedback': form.cleaned_data['feedback']})
        superusers = User.objects.filter(is_superuser=True)
        superusers_emails = [user.email for user in superusers]
        email = EmailMessage(
            'Thank you for contacting us.',
            template_email,
            settings.EMAIL_HOST_USER,
            [form.cleaned_data['email']],
            superusers_emails,
        )
        email.fail_silently=False
        email.send()

        return super(ContactView, self).form_valid(form)


def contact_done(request):
    return render (request, 'tisdac_app/contact_done.html')


def upcoming_events(request):
    events = []
    for event in Events.objects.select_related('department').all().order_by('date'):
        event.save()
        if event.date.timestamp() > datetime.now().timestamp():
            events.append(event)
    departments = set()
    for event in events:
        departments.add(event.department)
    return render(request, 'tisdac_app/upcoming_events.html', {'events': events,
                                                               'departments': departments})


class ShowOneEventView(View):
    def get(self, request, slug_event:str):
        event = get_object_or_404(Events, slug=slug_event)
        events = []
        for ev in Events.objects.select_related('department').all():
            if ev.date.timestamp() > datetime.now().timestamp():
                events.append(ev)
        if len(events) > 3:
            events = random.sample(events, 3)
        form = EventForm()
        return render(request, 'tisdac_app/event_detail.html', {
            'event': event,
            'events': events,
            'form': form,
        })

    def post(self, request, slug_event:str):
        event = get_object_or_404(Events, slug=slug_event)
        events = []
        for ev in Events.objects.select_related('department').all():
            if ev.date.timestamp() > datetime.now().timestamp():
                events.append(ev)
        if len(events) > 3:
            events = random.sample(events, 3)
        form = EventForm(request.POST)
        if form.is_valid():

            visitor = Visitor(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email']
            )

            if Visitor.objects.filter(name=visitor.name, email=visitor.email, phone=visitor.phone).first():
                event.visitors.add(
                    Visitor.objects.filter(name=visitor.name, email=visitor.email, phone=visitor.phone).first())
                event.save()
            else:
                visitor.save()
                event.visitors.add(visitor)
                event.save()

            #Sending Email
            template_email_recipient = render_to_string('email/email_booking_recipient.html', {'name': form.cleaned_data['name'],
                                                                                         'visitor': visitor,
                                                                                         'event': event,
                                                                                         'visitors': event.visitors})
            template_email_team = render_to_string('email/email_booking_team.html',
                                                        {'name': form.cleaned_data['name'],
                                                         'visitor': visitor,
                                                         'event': event,
                                                         'visitors': event.visitors.all()})

            superusers = User.objects.filter(is_superuser=True)
            superusers_emails = [user.email for user in superusers]
            email = EmailMessage(
                'Looking forward to seeing you',
                template_email_recipient,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']],
            )
            email.fail_silently = False
            email.send()

            email = EmailMessage(
                'You have a new visitor',
                template_email_team,
                settings.EMAIL_HOST_USER,
                [event.department.leader_email],
                superusers_emails,
            )
            email.fail_silently = False
            email.send()

            return HttpResponseRedirect('done')
        else:
            form = EventForm()
        return render(request, 'tisdac_app/event_detail.html', {
            'event': event,
            'events': events,
            'form': form,
        })

#Не используется. Вместо нее класс ShowOneEventView
def show_one_event(request, slug_event:str):
    event = get_object_or_404(Events, slug=slug_event)
    events = []
    for ev in Events.objects.all():
        if ev.date.timestamp() > datetime.now().timestamp():
            events.append(ev)
    if len(events) > 3:
        events = random.sample(events, 3)
#Регистрация нового посетителя
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            visitor = Visitor(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email']
            )
            if Visitor.objects.filter(name=visitor.name, email=visitor.email, phone=visitor.phone).first():
                event.visitors.add(Visitor.objects.filter(name=visitor.name, email=visitor.email, phone=visitor.phone).first())
                event.save()
            else:
                visitor.save()
                event.visitors.add(visitor)
                event.save()
            return HttpResponseRedirect('done')

    else:
        form = EventForm()
    return render(request, 'tisdac_app/event_detail.html', {
        'event': event,
        'events': events,
        'form': form,
        })


def show_one_event_done(request):
    events = []
    for ev in Events.objects.select_related('department').all():
        if ev.date.timestamp() > datetime.now().timestamp():
            events.append(ev)
    if len(events) > 3:
        events = random.sample(events, 3)
    return render(request, 'tisdac_app/event_detail_done.html', {'events': events})


def activities(request):
    departments = [i for i in Department.objects.all() if i.status == 'Active']
    return render(request, 'tisdac_app/activities.html', {'departments': departments})


def show_one_activity(request, slug_department:str):

    department = get_object_or_404(Department, slug=slug_department)
    departments = [i for i in Department.objects.all() if i.status == 'Active']
    departments = random.sample(departments, 3)

    events = []
    for event in Events.objects.select_related('department').all():
        event.save()
        if event.date.timestamp() > datetime.now().timestamp() and event.department == department:
            events.append(event)

    return render(request, 'tisdac_app/activity_detail.html', {
        'department': department,
        'departments': departments,
        'events': events
    })


def services(request):
    for service in Service.objects.all():
        service.save()
    services = Service.objects.all()
    return render(request, 'tisdac_app/services.html', {'services': services})


def show_one_service(request, slug_service:str):
    service = get_object_or_404(Service, slug=slug_service)
    services = Service.objects.all()
    if len(services) > 3:
        services = random.sample(services, 3)

    return render(request, 'tisdac_app/service_detail.html', {
        'service': service,
        'services': services
    })

def news(request):
    news = News.objects.select_related('department').all().filter(publish='YES').order_by('-date')
    departments = set()
    for n in news:
        departments.add(n.department)
    if request.user.is_authenticated:
        news = News.objects.select_related('department').all().exclude(publish='NO').order_by('-date')
        departments = set()
        for n in news:
            departments.add(n.department)
    return render(request, 'tisdac_app/news.html', {'news': news,
                                                          'departments': departments})

#Использую функцию news вместо класса
class ListNews(ListView):
    template_name = 'tisdac_app/news.html'
    model = News
    paginate_by = 15
    context_object_name = 'news'

    queryset = News.objects.all().filter(publish='YES').order_by('-date')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListNews, self).get_context_data(**kwargs)
        departments = set()
        for n in ListNews.queryset:
            departments.add(n.department)
        context['departments'] = departments
        #if request.user.is_authenticated():
        return context


def show_one_article(request, article_id):
    article = get_object_or_404(News, id=article_id)
    news = News.objects.select_related('department').all().filter(publish='YES')
    if request.user.is_authenticated:
        news = News.objects.select_related('department').all().exclude(publish='NO').order_by('-date')
    if len(news) > 3:
        news = random.sample(list(news), 3)


    return render(request, 'tisdac_app/news_detail.html', {
        'news': article,
        'news_set': news
    })


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'tisdac_app/register.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # Sendind Email
        template_email_registered = render_to_string('email/email_registration.html',
                                               {'username': form.cleaned_data['username'],
                                                'email': form.cleaned_data['email'],
                                                'password': form.cleaned_data['password1'],
                                                })

        email = EmailMessage(
            'Registration on tisdac.ee',
            template_email_registered,
            settings.EMAIL_HOST_USER,
            [form.cleaned_data['email']],
        )
        email.fail_silently = False
        email.send()

        return HttpResponseRedirect('/')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    #form_class = LoginUserForm
    template_name = 'tisdac_app/login.html'

    def get_success_url(self):
        return '/'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('login')
