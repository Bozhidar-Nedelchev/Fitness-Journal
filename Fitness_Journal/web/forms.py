from django import forms
from .models import ProgressPhoto, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age']


class MealForm(forms.Form):
    number_of_meals = forms.IntegerField(
        label='Number of Meals (1 to 5)',
        min_value=1,
        max_value=5,
    )

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)

        if self.is_bound and 'number_of_meals' in self.data:
            meal_count = int(self.data['number_of_meals'])
            for i in range(1, meal_count + 1):
                meal_field_name = f'Meal_{i}'
                if meal_field_name not in self.fields:
                    self.fields[meal_field_name] = forms.CharField(label=f'Meal {i}')


class ProgressPhotoForm(forms.ModelForm):
    class Meta:
        model = ProgressPhoto
        fields = ['photo', 'caption']