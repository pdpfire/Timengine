from django import forms
from .models import DiaryEntry


# Class for new work flow
class TaskDetailForm(forms.Form):
    title = forms.CharField(label="Activity Title", required=False)
    taskdetails = forms.CharField(label="Activity Details", widget=forms.Textarea, required=False)
    goal = forms.ChoiceField(label="Select Existing Goal", required=False)
    new_goal = forms.CharField(label="Or Create New Goal", required=False)

    # *** ADDED THE 'feeling' FIELD HERE ***
    feeling = forms.ChoiceField(
        label="How did you feel during the Task?",
        choices=DiaryEntry.FEELING_CHOICES, # Uses the choices defined in your DiaryEntry model
        required= True, # Set to True if you want to make this a mandatory field
        initial='neutral', # Sets the default selected option in the dropdown
        widget=forms.Select(attrs={'class': 'form-control'}) # Add Bootstrap styling
    )

    def __init__(self, *args, **kwargs):
        goals = kwargs.pop('goals', [])
        super().__init__(*args, **kwargs)
        self.fields['goal'].choices = [('', '--- Select Goal ---')] + [(g, g) for g in goals]

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('goal') and not cleaned.get('new_goal'):
            raise forms.ValidationError("You must either select or create a goal.")
        return cleaned


# def clean(self):
#     cleaned_data = super().clean()
#     goal = cleaned_data.get("goal")
#     new_goal = cleaned_data.get("new_goal")

#     if not goal and not new_goal:
        # Attach the error to the 'goal' field instead of raising global form error
#         self.add_error("goal", "You must either select or create a goal.")


