from django.db import models
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .models import Course, Slider, Video, Comment
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CourseForm, VideoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .models import Transaction
from academy import settings 
from django.utils.translation import gettext as _
from django.utils import translation
import stripe

# Create your views here.


def set_language(request):
    language = request.POST.get('language')
    translation.activate(language)
    response = HttpResponseRedirect(reverse_lazy('home'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response



@login_required
def notperm(request):
    return render(
        request,
        'notaccess.html'
    )


def user_is_staff(user):
    return user.is_staff


def index(request):
    slider = Slider.objects.all()


    return render(
        request,
        'index.html',
        {
            'slider': slider,
        }
    )


def about(request):
    aboutus_image = Slider.objects.first()

    return render(request, 'about.html', {'image': aboutus_image,})


def course(request):

    query = request.GET.get('query')

    where = {}
    if query:
        where['name__icontains'] = query

    course = Course.objects.filter(**where)

    return render(
        request,
        'course.html',
        {
            'courses': course
        }
    )


@login_required
def course_list(request, pk):

    query = request.GET.get('query')

    where = {}
    if query:
        where['name__icontains'] =  query


    user_course = request.user.profile.courses


    if user_course is not None:
        if pk in user_course:
            video = Video.objects.filter(course=pk, **where).select_related('course')
            course = Course.objects.get(pk=pk)
            return render(
                request,
                'course_list.html',
                {
                    'videos': video,
                    'cou': course,
                }
            )
        else:
            course1 = Course.objects.get(pk=pk)

            return render(
                request,
                'course/checkout.html',
                {
                    'course': course1
                }
            )
    else:
        course1 = Course.objects.get(pk=pk)

        return render(
            request,
            'course/checkout.html',
            {
                'course': course1
            }
        )  
         



    
@login_required
def course_videos(request, pk):
    videos = Video.objects.filter(pk=pk).all()

    courses_id = []

    for video1 in videos:
        courses_id.append(video1.course_id)


    user_courses = request.user.profile.courses


    if user_courses is not None:
        if courses_id[0] in user_courses:
            for video in videos:
                return render(
                    request,
                    'course_page.html',
                    {
                        'video': video
                    }
                )
        else:
            course1 = Course.objects.get(pk=courses_id[0])

            return render(
                request,
                'course/checkout.html',
                {
                    'course': course1
                }
            )
    elif courses_id is None or user_courses is None:
        course1 = Course.objects.get(pk=courses_id[0])

        return render(
            request,
            'course/checkout.html',
            {
                'course': course1
            }
        )    
    else:
        return redirect(reverse_lazy('login')) 



@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/create.html'
    success_url = reverse_lazy('course')

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/update.html'
    success_url = reverse_lazy('course')

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'course/delete.html'
    success_url = reverse_lazy('course')

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class VideoCreateView(CreateView):
    model = Video
    fields = ['title', 'desc', 'video', 'course']
    http_method_names = ['post']
    

    def get_success_url(self):
        return reverse('course_list', args=[self.object.course.id])

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'video/update.html'

    def get_success_url(self):
        return reverse('course_list', args=[self.object.course_id])

@method_decorator(user_passes_test(user_is_staff, login_url=reverse_lazy('notaccess')), name='dispatch')
class VideoDeleteView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'video/delete.html'
    
    def get_success_url(self):
        return reverse('course_list', args=[self.object.course_id])
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['video', 'user', 'message']
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('course_page', args=[self.object.video.id]) 
        
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('course_page', args=[self.object.video.id]) 
    
@login_required
def checkout_complete(request):

    try:
        course_id = request.user.profile.courses[-1]

        return render(
            request,
            'course/checkout-complete.html',
            {
                'id': course_id
            }
        )
    except:
        return redirect(reverse_lazy('checkout.complete'))


@login_required
def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def stripe_transaction(request):
    transaction = make_transaction(request)

    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information.')
        }, status=400)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount = int(transaction.course.price * 100),
        currency = settings.CURRENCY,
        payment_method_types = ['card'],
        metadata = {
            'transaction': transaction.id
        }
    )
    return JsonResponse({
        'client_secret': intent['client_secret']
    })


@login_required
def make_transaction(request):

    return Transaction.objects.create(
        user = request.user,
        course_id = request.POST['course'],
    )