from django.urls import path

from Fitness_Journal.web.views import MainUserView, ProfileUpdateView, UploadProgressPhotoView, UserPhotosListView, MealFormView, DisplayMealsView, MyProfileView, ContactsView, WorkoutsListView, WorkoutCreateView

urlpatterns=(
    path('', MainUserView.as_view(), name='main_view'),
    path('diet/', MealFormView.as_view(), name='custom_diet'),
    path('my-meals/', DisplayMealsView.as_view(), name='added_meal'),
    path('upload_progress_photo/', UploadProgressPhotoView.as_view(), name='upload_progress_photo'),
    path('added_photos/', UserPhotosListView.as_view(), name='added_photos'),
    path('profile/', MyProfileView.as_view(), name='my_profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('add_workout/', WorkoutCreateView.as_view(), name='add_workout'),
    path('workouts/', WorkoutsListView.as_view(), name='workouts_list'),

)
