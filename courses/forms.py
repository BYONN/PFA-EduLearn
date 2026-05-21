from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'categorie', 'cover_image', 'content']
        labels = {
            'name': 'Nom du cours',
            'description': 'Description courte',
            'categorie': 'Catégorie',
            'cover_image': 'Image de couverture',
            'content': 'Contenu du cours',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-0 py-3 px-3 shadow-none', 'style': 'background-color: #f3f4f6; border-radius: 8px;', 'placeholder': 'Ex: Introduction à Python'}),
            'description': forms.Textarea(attrs={'class': 'form-control border-0 py-3 px-3 shadow-none', 'style': 'background-color: #f3f4f6; border-radius: 8px;', 'rows': 3, 'placeholder': 'Décrivez brièvement le contenu du cours...'}),
            'categorie': forms.Select(attrs={'class': 'form-select border-0 py-3 px-3 shadow-none', 'style': 'background-color: #f3f4f6; border-radius: 8px;'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control border-0 py-2 px-3 shadow-none', 'style': 'background-color: #f3f4f6; border-radius: 8px;'}),
            # 'content' automatically uses CKEditorWidget because of RichTextUploadingField
        }
