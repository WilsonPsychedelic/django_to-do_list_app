from django import forms
from .models import Todo, Category


class TodoForm(forms.ModelForm):
    class Meta:
        model  = Todo
        fields = ['title', 'description', 'priority', 'due_date', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 '
                         'bg-white text-gray-800 placeholder-gray-400',
                'placeholder': 'What needs to be done?',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 '
                         'bg-white text-gray-800 placeholder-gray-400',
                'placeholder': 'Add a description (optional)…',
                'rows': 3,
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 '
                         'bg-white text-gray-800',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 '
                         'bg-white text-gray-800',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 '
                         'bg-white text-gray-800',
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 '
                         'bg-white text-gray-800 placeholder-gray-400',
                'placeholder': 'e.g. Work, Personal, Shopping…',
            }),
        }