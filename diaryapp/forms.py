from django import forms
from .models import DiaryEntry

#class DiaryEntryForm(forms.ModelForm):
#    class Meta:
#        model = DiaryEntry
#        fields = '__all__'

class DiaryEntryForm(forms.Form):
    title = forms.CharField(label="Task Title")
    taskdetails = forms.CharField(label="Task Details", widget=forms.Textarea)


# class TableSelectForm(forms.Form):
#     table_name = forms.ChoiceField(label="Choose Existing Table", required=False)
#     new_table = forms.BooleanField(required=False, label="Create New Table?")
#     #new_table_name = forms.CharField(required=False, label="New Table Name")
#     auth_keyword = forms.CharField(required=False, label="Authorization Code")
#     new_table_name = forms.CharField(
#         required=False,
#         label="New Table Name",
#         max_length=50,
#         widget=forms.TextInput(attrs={"placeholder": "e.g. DailyLog2025"})
   

#     def __init__(self, *args, **kwargs):
#         tables = kwargs.pop('tables', [])
#         super().__init__(*args, **kwargs)
#         self.fields['table_name'].choices = [(t, t) for t in tables]

#     def clean(self):
#         cleaned_data = super().clean()
#         new_table = cleaned_data.get("new_table")
#         new_table_name = cleaned_data.get("new_table_name")
#         auth_keyword = cleaned_data.get("auth_keyword")

#         if new_table:
#             if not new_table_name:
#                 self.add_error("new_table_name", "This field is required when creating a new table.")
#             if not auth_keyword:
#                 self.add_error("auth_keyword", "Authorization Code is required for new tables.")

# Class for new work flow
class TaskDetailForm(forms.Form):
    title = forms.CharField(label="Activity Title", required=False)
    taskdetails = forms.CharField(label="Activity Details", widget=forms.Textarea, required=False)
    goal = forms.ChoiceField(label="Select Existing Goal", required=False)
    new_goal = forms.CharField(label="Or Create New Goal", required=False)

    def __init__(self, *args, **kwargs):
        goals = kwargs.pop('goals', [])
        super().__init__(*args, **kwargs)
        self.fields['goal'].choices = [('', '--- Select Goal ---')] + [(g, g) for g in goals]

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('goal') and not cleaned.get('new_goal'):
            raise forms.ValidationError("You must either select or create a goal.")
        return cleaned


def clean(self):
    cleaned_data = super().clean()
    goal = cleaned_data.get("goal")
    new_goal = cleaned_data.get("new_goal")

    if not goal and not new_goal:
        # Attach the error to the 'goal' field instead of raising global form error
        self.add_error("goal", "You must either select or create a goal.")


