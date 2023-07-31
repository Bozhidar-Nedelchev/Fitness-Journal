from datetime import date
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as view
from django.shortcuts import render
from .models import ProgressPhoto
from .forms import ProgressPhotoForm
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MealPlan,MealEntry
from .forms import MealForm,ProfileForm
from .models import Profile

class MainUserView(auth_views.TemplateView):
    template_name = 'web/main.html'

class ProfileUpdateView(view.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_update.html'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('profile_update')


class MealFormView(LoginRequiredMixin,view.ListView):
        template_name = 'web/diet.html'

        def get(self, request):
            form = MealForm()
            return render(request, self.template_name, {'form': form})

        def post(self, request):
            form = MealForm(request.POST)
            if form.is_valid():
                meals_count = form.cleaned_data.get('number_of_meals')
                meal_data = []

                for i in range(1, meals_count + 1):
                    meal_field_name = f'meal_{i}'
                    meal_data.append(request.POST.get(meal_field_name, ''))


                user = request.user
                current_date = date.today()

                meal_plan = MealPlan.objects.create(user=user, date=current_date)

                for meal_name in meal_data:
                    MealEntry.objects.create(meal_plan=meal_plan, meal_name=meal_name)

                return redirect('added_meal')
            return render(request, self.template_name, {'form': form})
class DisplayMealsView(LoginRequiredMixin, view.View):
    template_name = 'web/addedmeal.html'

    def get(self, request):
        user = request.user
        meal_plans = MealPlan.objects.filter(user=user)

        context = {
            'meal_plans': meal_plans,
        }

        return render(request, self.template_name, context)

#moje da se dobavi i data na upload na snimkata!!!
class UploadProgressPhotoView(LoginRequiredMixin,view.FormView):
    template_name = 'web/upload_progress_photo.html'
    form_class = ProgressPhotoForm
    success_url = 'web/photos_page.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:

            return render(request, 'app_auth/login.html')

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():

            progress_photo = form.save(commit=False)
            progress_photo.user = request.user
            image_field = form.cleaned_data['photo']
            image = Image.open(image_field)
            output_size = (500, 300)
            image.thumbnail(output_size)
            output_buffer = BytesIO()
            image.save(output_buffer, format='JPEG')
            output_buffer.seek(0)


            resized_image = InMemoryUploadedFile(
                output_buffer,
                'ImageField',
                image_field.name,
                'image/jpeg',
                len(output_buffer.getvalue()),
                None
            )
            progress_photo.photo = resized_image
            progress_photo.save()


            uploaded_photos = ProgressPhoto.objects.filter(user=request.user)



            return redirect('added_photos')
        return render(request, self.template_name, {'form': form})


class UserPhotosListView(LoginRequiredMixin,view.ListView):
    model = ProgressPhoto
    template_name = 'web/photos_page.html'
    context_object_name = 'user_photos'

    def get_queryset(self):
        return ProgressPhoto.objects.filter(user=self.request.user)
