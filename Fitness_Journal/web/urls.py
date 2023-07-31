from django.urls import path

from Fitness_Journal.web.views import MainUserView,ProfileUpdateView,UploadProgressPhotoView,UserPhotosListView,MealFormView,DisplayMealsView

urlpatterns=(
    path('', MainUserView.as_view(), name='main_view'),
    path('diet/', MealFormView.as_view(), name='custom_diet'),
    path('my-meals/', DisplayMealsView.as_view(), name='added_meal'),
    path('upload_progress_photo/', UploadProgressPhotoView.as_view(), name='upload_progress_photo'),
    path('added_photos/', UserPhotosListView.as_view(), name='added_photos'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

)
