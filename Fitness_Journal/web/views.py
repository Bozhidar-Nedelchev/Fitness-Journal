from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
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
from django.views.generic import TemplateView
import random


class MainUserView(TemplateView):
    template_name = 'web/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotes = [
                "“I hated every minute of training, but I said, ‘Don’t quit. Suffer now and live the rest of your life as a champion.” – Muhammad Ali",
                "“We are what we repeatedly do. Excellence then is not an act but a habit.” –Aristotele",
                "“The body achieves what the mind believes.” – Napoleon Hill",
                "“The hard days are the best because that’s when champions are made, so if you push through, you can push through anything.” – Dana Vollmer",
                "“If you don’t find the time, if you don’t do the work, you don’t get the results.” – Arnold Schwarzenegger",
                "“Dead last finish is greater than did not finish, which trumps did not start.” — Unknown",
                "“Push harder than yesterday if you want a different tomorrow.” – Vincent Williams Sr.",
                "“The real workout starts when you want to stop.” – Ronnie Coleman",
                "“Take care of your body. It’s the only place you have to live.” — Jim Rohn",
                "“I’ve failed over and over again in my life and that is why I succeed.” – Michael Jordan",
                "“Once you are exercising regularly, the hardest thing is to stop it.” – Erin Gray",
                "“The secret of getting ahead is getting started.” — Mark Twain",
                "“Exercise should be regarded as tribute to the heart” – Gene Tunney",
                "“You’re going to have to let it hurt. Let it suck. The harder you work, the better you will look. Your appearance isn’t parallel to how heavy you lift, it’s parallel to how hard you work.” –Joe Mangianello",
                "“Most people fail, not because of lack of desire, but, because of lack of commitment.” –Vince Lombardi",
                "“You miss one hundred percent of the shots you don’t take.” – Wayne Gretzky",
                "“If something stands between you and your success, move it. Never be denied.” – Dwayne “The Rock” Johnson",
                "“All progress takes place outside the comfort zone.”– Michael John Bobak",
                "“Just believe in yourself. Even if you don’t, just pretend that you do and at some point, you will.” – Venus Williams",
                "“The harder you work and the more prepared you are for something, you’re going to be able to persevere through anything.” – Carli Lloyd",
                "“Enduring means accepting. Accepting things as they are and not as you would wish them to be, and then looking ahead, not behind.” – Rafael Nadal",
                "“If you want something you’ve never had, you must be willing to do something you’ve never done.” – Thomas Jefferson",
                "“The resistance that you fight physically in the gym and the resistance that you fight in life can only build a strong character.” – Arnold Schwarzenegger",
                "“Continuous improvement is better than delayed perfection.” – Mark Twain",
                "“Once you learn to quit, it becomes a habit.” – Vince Lombardi",
                "“It’s hard to beat a person who never gives up.” – Babe Ruth",
                "“Do something today that your future self will thank you for.” — Sean Patrick Flanery",
                "“Success is usually the culmination of controlling failure.” – Sylvester Stallone",
                "“Think of your workouts as important meetings you schedule with yourself. Bosses don’t cancel” – Unknown",
                "“Workout till you feel that pain and soreness in muscles. This one is good pain. No pain, no gain.” – Invajy",
                "“Confidence comes from discipline and training.” – Robert Kiyosaki",
                "“I don’t count my sit-ups. I only start counting when it starts hurting because they’re the only ones that count.”–Muhammad Ali",
                "“What hurts today makes you stronger tomorrow” –Jay Cutler",
                "“Strength does not come from physical capacity. It comes from an indomitable will” –Mahatma Gandhi",
                "“You must expect things of yourself before you can do them.” – Michael Jordan",
                "“The last three or four reps is what makes the muscle grow. This area of pain divides a champion from someone who is not a champion.” – Arnold Schwarzenegger",
                "“If you fail to prepare, you’re prepared to fail.” – Mark Spitz",
                "“Motivation is what gets you started. Habit is what keeps you going.” – Jim Ryun",
                "“A champion is someone who gets up when they can’t.” – Jack Dempsey",
                "“The difference between the impossible and the possible lies in a person’s determination.” – Tommy Lasorda",
                "“When you have a clear vision of your goal, it’s easier to take the first step toward it.” – LL Cool J",
                "“When I feel tired, I just think about how great I will feel once I finally reach my goal.” – Michael Phelps",
                "“You have to think about it before you can do it. The mind is what makes it all possible.” – Kai Greene",
                "“The only bad workout is the one that didn’t happen.” – Unknown",
                "“Don’t be afraid of failure. This is the way to succeed.” – LeBron James",
                "“You should never stay at the same level. Always push yourself to the next.” – Marnelli Dimzon",
                "“You did not wake up today to be mediocre.” – Robin Arzon",
                "“Action is the foundational key to all success.” – Pablo Picasso",
                "“If it doesn’t challenge you, it doesn’t change you.” – Fred DeVito",
                "“You can either suffer the pain of discipline or the pain of regret.” –Jim Rohn",
                "“We can push ourselves further. We always have more to give.” – Simone Biles",
                "“If you want to be the best, you have to do things other people aren’t willing to do.” – Michael Phelps",
                "“Every champion was once a contender who refused to give up.” – Rock Balboa",
                "“The difference between try and triumph is a little ‘umph’.” – Marvin Phillips",
                "“If you are not pissed off for greatness, that just means you’re okay with being mediocre.” – Ray Lewis",
                "“Keep working even when no one is watching.” – Alex Morgan",
                "“Your health account, your bank account, they’re the same thing. The more you put in, the more you can take out. Exercise is king and nutrition is queen. Together you have a kingdom.” – Jack LaLanne",
                "“Don’t dream of winning. Train for it!” – Mo Farah",
                "“Most people give you right before the big break comes, don’t let that person be you.” – Michael Boyle",
                "“Discipline is the bridge between goals and accomplishment.” – Jim Rohn",
                "“Fitness is not about being better than someone else. It’s about being better than you used to be. – Khloe Kardashian",
                "“Exercise should be regarded as a tribute to the heart.” – Gene Tunney",
                "“Keep listening to your body. It will tell you when something is not okay.” – Emily Infeld",
                "“Whether you think you can, or you think you can’t. you are right” – Henry Ford",
                "“All our dreams can come true if we have the courage to pursue them.” – Walt Disney",
                "“Great things come from hard work and perseverance. No excuses.” – Kobe Bryant",
                "“Always make a total effort, even when the odds are against you.” – Arnold Palmer",
                "“Success is walking from failure to failure with no loss of enthusiasm.” –Winston Churchill",
                "“Your mind will quit a thousand times before your body will.” – Reginald Red",
                "“I’ve grown most not from victories, but setbacks. If winning is God’s reward, then losing is how he teaches us.” – Serena Williams",
                "“Set your goals high, and don’t stop until you get there.” – Bo Jackson",
                "“Physical fitness can neither be achieved by wishful thinking nor outright purchase.” – Joseph Pilates",
                "“If you take time to realize what your dream is and what you really want in life — no matter what it is, whether it’s sports or in other fields — you have to realize that there is always work to do, and you want to be the hardest working person in whatever you do, and you put yourself in a position to be successful. And you have to have a passion about what you do.” – Stephen Curry",
                "“You shall gain, but you shall pay with sweat, blood, and vomit.” – Pavel Tsatsouline",
                "“You have to push past your perceived limits, push past that point you thought was as far as you can go.” – Drew Brees",
                "“Get ready, be prepared. So when opportunities finally show themselves, you’ll be able to own them.” – Hannah Gabriels",
                "“You dream. You plan. You reach. There will be obstacles. There will be doubters. There will be mistakes. But with hard work, with belief, with confidence and trust in yourself and those around you, there are no limits.” – Michael Phelps",
                "“Be Humble. Be Hungry. And always be the hardest worker in the room.” – Dwayne ‘The Rock’ Johnson",
                "“Some people want it to happen, some wish it would happen, others make it happen.” – Michael Jordan",
                "“A year from now you may wish you had started today.” – Karen Lamb",
                "“A goal is just an awesome way to force growth on yourself” – Deena Kastor",
                "“If you do not believe in yourself, no one will do it for you” – Kobe Bryant",
                "“Our bodies are gardens, our wills are our gardeners.” – William Shakespeare",
                "“Get comfortable with being uncomfortable!” – Jillian Michaels",
                "“Time, Effort, Sacrifice, and Sweat. How will you pay for your goals?” – Usain Bolt",
                "“He who is not courageous enough to take risks, will accomplish nothing in life.” – Muhammad Ali",
                "“It’s supposed to be hard. If it wasn’t hard, everyone would do it. The hard is what makes it great.”  — Tom Hanks",
                "“The purpose of training is to tighten up the slack, toughen the body, and polish the spirit.” — Morihei Ueshiba",
                "“Put all excuses aside and remember this: You are capable.” – Zig Ziglar",
                "“The groundwork for all happiness is good health.” – Leigh Huntfs",
                "“Success usually comes to those who are too busy to be looking for it.” — Henry David Thoreau",
                "“The only place where success comes before work is in the dictionary.” – Vidal Sassoon",
                "“The clock is ticking. Are you becoming the person you want to be?” –Greg Plitt",
                "“The successful warrior is the average man, with laser-like focus.” – Bruce Lee",
                "“Pain is temporary. Quitting lasts forever.” – Lance Armstrong",
                "“Physical fitness is not only one of the most important keys to a healthy body, it is the basis of dynamic and creative intellectual activity.” – John F. Kennedy",
                "“No matter how many mistakes you make or how slow you progress, you are still way ahead of everyone who isn’t trying.” – Tony Robbins",
                "“Making excuses burns zero calories per hour.” – Unknown",
                "“The only person you are destined to become is the person you decide to be.” – Ralph Waldo Emerson",
                "“Great works are performed, not by strength, but by perseverance.” – Samuel Johnson"
        ]
        random_quote = random.choice(quotes)

        context['random_quote'] = random_quote

        return context


class ProfileUpdateView(LoginRequiredMixin, view.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_update.html'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('my_profile')


class MealFormView(LoginRequiredMixin, view.ListView):
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
                    meal_field_name = f'Meal_{i}'
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

    def post(self, request, *args, **kwargs):
        if 'delete_selected' in request.POST:
            selected_meal_plans_ids = request.POST.getlist('selected_meal_plans')
            MealPlan.objects.filter(id__in=selected_meal_plans_ids, user=request.user).delete()

        return HttpResponseRedirect(reverse('added_meal'))


class UploadProgressPhotoView(LoginRequiredMixin, view.FormView):
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

            return redirect('added_photos')

        return render(request, self.template_name, {'form': form})


class UserPhotosListView(LoginRequiredMixin, view.ListView):
    model = ProgressPhoto
    template_name = 'web/photos_page.html'
    context_object_name = 'user_photos'

    def get_queryset(self):
        return ProgressPhoto.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if 'delete_selected' in request.POST:
            selected_photos_ids = request.POST.getlist('selected_photos')
            ProgressPhoto.objects.filter(id__in=selected_photos_ids, user=request.user).delete()

        return HttpResponseRedirect(reverse('added_photos'))


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'my_profile.html'


class ContactsView(TemplateView):
    template_name = 'contacts.html'