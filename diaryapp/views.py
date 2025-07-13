
from django.shortcuts import render, redirect
from django.utils import timezone
from django import forms
from django.db import router
from .models import DiaryEntry
from datetime import datetime
from .forms import TaskDetailForm
from django.utils import timezone


# ---- FORMS ---- #


# class DiaryEntryForm(forms.Form):
#     title = forms.CharField(label="Task Title")
#     taskdetails = forms.CharField(label="Task Details", widget=forms.Textarea)


# ---- HELPERS ---- #

# def generate_tbn_from_tables(tables):
#     tbn = ''
#     for idx, name in enumerate(tables, start=1):
#         if idx == 1:
#             tbn = name[1].lower()
#         else:
#             tbn += name[0].lower()
#     return tbn

# ---- VIEWS ---- #
# Home page view
def instructions(request):
    return render(request, 'instructions.html')

 
# new workflow Starting task click
def start_task(request):
    request.session['strtime'] = timezone.now().isoformat()
    return redirect('task_in_progress')

# new workflow Starting task page show
def task_in_progress(request):
    print("🧭 Entered task_in_progress view at:", timezone.now())

    strtime = request.session.get('strtime')
    if not strtime:
        print("❌ strtime missing in session")
        strtime = timezone.now().isoformat()  # fallback
    
    print("✅ strtime in session:", strtime)

    return render(request, 'task_in_progress.html', {'strtime': strtime,'strtime': request.session['strtime']})

# def task_in_progress(request):
#     strtime = request.session.get("start_time")  # or however you're storing it
#     if not strtime:
#         strtime = timezone.now().isoformat()  # fallback
#     return render(request, 'task_in_progress.html', {
#         'strtime': strtime,
#     })

# new workflow Starting task page show
def done_with_task(request):
    print("✅ Entered done_with_task view at:", timezone.now())
    print("🧠 DWT SESSION Start:\n", dict(request.session))
    strtime_str = request.session.get('strtime')
    if not strtime_str:
        return redirect('start_task')

    strtime = datetime.fromisoformat(strtime_str)
    now = timezone.now()

    # ✅ Tasktime is NOW - strtime
    if 'task_time' not in request.session:
        task_time = now - strtime
        request.session['task_time'] = str(task_time)

    # ✅ Detail Start Time begins now (page load)
    if 'detail_start_time' not in request.session:
        request.session['detail_start_time'] = timezone.now().isoformat()
    elif datetime.fromisoformat(strtime_str) > datetime.fromisoformat(request.session.get('detail_start_time')):
        request.session['detail_start_time'] = timezone.now().isoformat()

    # if 'detail_start_time' in request.session:
    #     if datetime.fromisoformat(strtime_str) > datetime.fromisoformat(detail_start_time):
    #         request.session['detail_start_time'] = timezone.now().isoformat()
    # else:
    #     request.session['detail_start_time'] = timezone.now().isoformat()

    # Get distinct goal values
    goals = DiaryEntry.objects.using('diary').values_list('goal', flat=True).distinct().order_by('goal')

    if request.method == 'POST':
        form = TaskDetailForm(request.POST, goals=goals)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            return redirect('finish_task')
    else:
        form = TaskDetailForm(goals=goals)
    
    print("🧠 DWT SESSION End:\n", dict(request.session))
    return render(request, 'done_with_task.html', {
        'form': form,
        'task_time': request.session['task_time'],
        'strtime': request.session['strtime'],}
    )


# new workflow Starting task page show
def finish_task(request):
    print("🧠 FINISH SESSION Strat:\n", dict(request.session))
    try:
        strtime = datetime.fromisoformat(request.session.get('strtime'))
        task_time = request.session.get('task_time')
        detail_start_time = datetime.fromisoformat(request.session.get('detail_start_time'))
        end_time = timezone.now()

        # ✅ Calculate detail duration
        detail_time = end_time - detail_start_time

        form_data = request.session.get('form_data')
        goal = form_data.get('new_goal') or form_data.get('goal')

        # ✅ Save entry
        DiaryEntry.objects.using('diary').create(
            strtime=strtime,
            title=form_data.get('title'),
            tasktime=task_time,
            taskdetails=form_data.get('taskdetails'),
            detailtime=str(detail_time),
            endtime=end_time,
            goal=goal
        )
        
        print("🧠 FINISH SESSION END:\n", dict(request.session))
        # ✅ Clear session
        for key in ['strtime', 'task_time', 'detail_start_time', 'form_data']:
            request.session.pop(key, None)

        return redirect('read_diary')

    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


def read_diary(request):
    goal_filter = request.GET.get('goal', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    # fetch distinct goal values for dropdown
    all_goals = DiaryEntry.objects.using('diary').values_list('goal', flat=True).distinct().order_by('goal')

    entries = DiaryEntry.objects.using('diary').all()

    if goal_filter:
        entries = entries.filter(goal=goal_filter)

    if start_date:
        entries = entries.filter(strtime__date__gte=start_date)
    if end_date:
        entries = entries.filter(strtime__date__lte=end_date)

    entries = entries.order_by('-id')

    return render(request, 'read.html', {
        'entries': entries,
        'goal_filter': goal_filter,
        'start_date': start_date,
        'end_date': end_date,
        'all_goals': all_goals,
    })


