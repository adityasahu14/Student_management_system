from django import forms
from .models import Query, Subject, Class
from accounts.models import User

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'section']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['class_ref', 'name', 'code', 'credits', 'teacher']
        labels = {'class_ref': 'Class'}
        
    def __init__(self, *args, **kwargs):
        institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        if institution:
            self.fields['teacher'].queryset = User.objects.filter(institution=institution, role='teacher')
            self.fields['class_ref'].queryset = Class.objects.filter(institution=institution)
from accounts.models import User

class StudentQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['teacher', 'subject', 'question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your question here...'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            subjects = Subject.objects.filter(class_ref=student.class_ref)
            teachers = [sub.teacher.id for sub in subjects if sub.teacher]
            
            self.fields['teacher'].queryset = User.objects.filter(id__in=teachers)
            self.fields['subject'].queryset = subjects
            self.fields['subject'].required = False
