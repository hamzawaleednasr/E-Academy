from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm, ProfileForm
from .models import Profile
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils import translation
import re
from academy import settings

# Create your views here.





class SwitchLangView(View):
  def dispatch(self, request, *args, **kwargs):
    lang = kwargs['lang']
    translation.activate(lang)
    next = request.GET.get('next')
    next = re.sub('ar|en', lang, next, 1)
    response = HttpResponseRedirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response




class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('profile')

    def form_valid(self, form):
        form.save()    # The User is now created

        # Create a Profile instance for that User
        Profile.objects.create(user=form.instance, profile_image=self.request.FILES['profile_image'])
        super(RegisterView, self).form_valid(form)
        return redirect('profile')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=request.user)
        return render(request, 'common/profile.html', {
            'form': form
        })