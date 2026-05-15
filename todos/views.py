from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo, Category
from .forms import TodoForm, CategoryForm


# ── List ────────────────────────────────────────────
@login_required
def todo_list(request):
    todos = Todo.objects.filter(owner=request.user)

    # ── search ──
    query = request.GET.get('q', '').strip()
    if query:
        todos = todos.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # ── filter by status ──
    status = request.GET.get('status', 'all')
    if status == 'completed':
        todos = todos.filter(completed=True)
    elif status == 'pending':
        todos = todos.filter(completed=False)

    # ── filter by priority ──
    priority = request.GET.get('priority', '')
    if priority in ('low', 'medium', 'high'):
        todos = todos.filter(priority=priority)

    # ── filter by category ──
    cat_id = request.GET.get('category', '')
    if cat_id.isdigit():
        todos = todos.filter(category_id=int(cat_id))

    # ── filter by due-date bucket ──
    due = request.GET.get('due', '')
    if due == 'overdue':
        from django.utils.timezone import now
        todos = todos.filter(due_date__lt=now().date(), completed=False)
    elif due == 'today':
        from django.utils.timezone import now
        todos = todos.filter(due_date=now().date())
    elif due == 'upcoming':
        from django.utils.timezone import now
        from datetime import timedelta
        today = now().date()
        todos = todos.filter(due_date__gte=today, due_date__lte=today + timedelta(days=7))

    completed_count = todos.filter(completed=True).count()
    pending_count   = todos.filter(completed=False).count()
    categories      = Category.objects.filter(owner=request.user)

    from django.utils.timezone import now
    return render(request, 'todos/todo_list.html', {
        'todos':           todos,
        'completed_count': completed_count,
        'pending_count':   pending_count,
        'categories':      categories,
        'query':           query,
        'status':          status,
        'priority':        priority,
        'cat_id':          cat_id,
        'due':             due,
        'today':           now().date(),                                          # used by "Overdue" badge in template
        'status_choices':   [('all','All'), ('pending','Pending'), ('completed','Completed')],
        'priority_choices': [('low','Low'), ('medium','Medium'), ('high','High')],
        'due_choices':      [('overdue','Overdue'), ('today','Today'), ('upcoming','This Week')],
    })


# ── Create ──────────────────────────────────────────
@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        # limit category choices to this user
        form.fields['category'].queryset = Category.objects.filter(owner=request.user)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
        form.fields['category'].queryset = Category.objects.filter(owner=request.user)
    return render(request, 'todos/todo_form.html', {'form': form})


# ── Update ──────────────────────────────────────────
@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        form.fields['category'].queryset = Category.objects.filter(owner=request.user)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
        form.fields['category'].queryset = Category.objects.filter(owner=request.user)
    return render(request, 'todos/todo_form.html', {'form': form})


# ── Delete ──────────────────────────────────────────
@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})


# ── Toggle ──────────────────────────────────────────
@login_required
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


# ── Categories ──────────────────────────────────────
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            # Return to the page that sent us here (todo form or list)
            next_url = request.GET.get('next', 'todo_list')
            return redirect(next_url)
    else:
        form = CategoryForm()
    return render(request, 'todos/category_form.html', {'form': form})