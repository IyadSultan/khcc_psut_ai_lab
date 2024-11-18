# projects/forms.py

from django import forms
from django.core.validators import URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Q
import mimetypes
from PIL import Image
from io import BytesIO
import os

from .models import (
    Project,
    Comment,
    UserProfile,
    Rating,
    Bookmark,
    ProjectAnalytics,
    Notification,
    Profile
)

class ProjectForm(forms.ModelForm):
    """
    Form for creating and editing projects.
    Includes validation for GitHub links and tag formatting.
    """
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., AI, Machine Learning, NLP)',
            'data-toggle': 'tooltip',
            'title': 'Add up to 5 tags to help others find your project'
        })
    )
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'tags', 'pdf_file', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
                'maxlength': '200',
                'data-toggle': 'tooltip',
                'title': 'Choose a descriptive title for your project'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project in detail...',
                'data-toggle': 'tooltip',
                'title': 'Explain what your project does, technologies used, and its purpose'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repository',
                'data-toggle': 'tooltip',
                'title': 'Link to your GitHub repository'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf',
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }

    def clean_github_link(self):
        """Validate GitHub repository URL"""
        url = self.cleaned_data['github_link']
        if not url.startswith(('https://github.com/', 'http://github.com/')):
            raise ValidationError('Please enter a valid GitHub repository URL')
        
        try:
            URLValidator()(url)
        except ValidationError:
            raise ValidationError('Please enter a valid URL')
        
        return url

    def clean_tags(self):
        """Validate and format tags"""
        tags = self.cleaned_data['tags']
        if not tags:
            return ''
        
        # Clean and validate tags
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = [x for x in tag_list if not (x in seen or seen.add(x))]
        
        if len(unique_tags) > 5:
            raise ValidationError('Please enter no more than 5 unique tags')
        
        if any(len(tag) > 20 for tag in unique_tags):
            raise ValidationError('Each tag must be less than 20 characters')
        
        return ', '.join(unique_tags)

    def clean_pdf_file(self):
        """Validate PDF file"""
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Check file size (10MB limit)
            if pdf_file.size > 10 * 1024 * 1024:
                raise ValidationError('PDF file must be smaller than 10MB')

            # Check file extension
            ext = os.path.splitext(pdf_file.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError('Only PDF files are allowed')

            # Check MIME type using mimetypes
            file_type, encoding = mimetypes.guess_type(pdf_file.name)
            if file_type != 'application/pdf':
                raise ValidationError('Invalid PDF file')

        return pdf_file

    def clean_featured_image(self):
        """Validate and process featured image"""
        image = self.cleaned_data.get('featured_image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 5MB')

            try:
                img = Image.open(image)
                
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Check dimensions
                if img.width > 2000 or img.height > 2000:
                    raise ValidationError('Image dimensions should not exceed 2000x2000 pixels')
                
                # Resize if larger than 1200px
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                # Save optimized image
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Return processed image
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return image

class CommentForm(forms.ModelForm):
    """
    Form for adding comments to projects.
    Includes validation for minimum content length.
    """
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
                'data-toggle': 'tooltip',
                'title': 'Share your thoughts, feedback, or questions'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data['content'].strip()
        if len(content) < 10:
            raise ValidationError('Comment must be at least 10 characters long')
        if len(content) > 1000:
            raise ValidationError('Comment must be less than 1000 characters')
        return content

    def clean_image(self):
        """Validate comment image"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (2MB limit)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 2MB')

            try:
                img = Image.open(image)
                
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Check dimensions
                if img.width > 1000 or img.height > 1000:
                    raise ValidationError('Image dimensions should not exceed 1000x1000 pixels')
                
                # Resize if larger than 800px
                if img.width > 800 or img.height > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                # Save optimized image
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Return processed image
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return image

class UserProfileForm(forms.ModelForm):
    """Form for user profile management"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'github_username', 'linkedin_url', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'maxlength': '500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you based?',
                'maxlength': '100'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username',
                'maxlength': '39'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.linkedin.com/in/your-profile'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_avatar(self):
        """Validate avatar file"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (5MB limit)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Avatar file must be smaller than 5MB')

            try:
                img = Image.open(avatar)
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Resize to standard avatar size
                output_size = (300, 300)
                img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(avatar.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Rating score'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience with this project (optional)',
                'maxlength': 500
            })
        }

    def clean_review(self):
        review = self.cleaned_data.get('review', '').strip()
        if len(review) > 500:
            raise ValidationError('Review must be less than 500 characters')
        return review

class BookmarkForm(forms.ModelForm):
    """Form for managing bookmarks"""
    class Meta:
        model = Bookmark
        fields = ['project']
        widgets = {
            'project': forms.HiddenInput()
        }

class ProjectSearchForm(forms.Form):
    """Form for project search and filtering"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search projects...',
            'aria-label': 'Search'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by tags (comma separated)',
            'aria-label': 'Tags'
        })
    )
    
    SORT_CHOICES = [
        ('-created_at', 'Newest first'),
        ('created_at', 'Oldest first'),
        ('-claps', 'Most popular'),
        ('title', 'Alphabetical'),
    ]
    
    sort = forms.ChoiceField(
        required=False,
        initial='-created_at',
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Sort projects'
        })
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            return [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        return []
    

################################

class FileValidationMixin:
    """Mixin for common file validation methods"""
    
    def validate_file_size(self, file, max_size_mb=5):
        if file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'File size must be no more than {max_size_mb}MB')
    
    def validate_file_type(self, file, allowed_types):
        file_type = mimetypes.guess_type(file.name)[0]
        if file_type not in allowed_types:
            raise ValidationError(f'File type {file_type} is not supported')
    
    def validate_image(self, image, max_dimension=2000):
        try:
            img = Image.open(image)
            if img.width > max_dimension or img.height > max_dimension:
                raise ValidationError(f'Image dimensions should not exceed {max_dimension}x{max_dimension} pixels')
            return img
        except Exception as e:
            raise ValidationError(f'Invalid image file: {str(e)}')

class AdvancedSearchForm(forms.Form):
    """Advanced search form with multiple filters"""
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, description, or author'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-role': 'tagsinput'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    min_claps = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    has_github = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-claps', 'Most popular'),
            ('-comment_count', 'Most discussed'),
            ('title', 'Alphabetical'),
            ('-rating_avg', 'Highest rated')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise ValidationError("End date should be greater than start date")
        
        return cleaned_data

# projects/filters.py

import django_filters
from django.db.models import Avg, Count, Q
from .models import Project

class ProjectFilter(django_filters.FilterSet):
    """FilterSet for advanced project filtering"""
    query = django_filters.CharFilter(method='filter_query')
    tags = django_filters.CharFilter(method='filter_tags')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_claps = django_filters.NumberFilter(field_name='claps', lookup_expr='gte')
    has_github = django_filters.BooleanFilter(method='filter_has_github')
    
    class Meta:
        model = Project
        fields = ['query', 'tags', 'date_from', 'date_to', 'min_claps', 'has_github']
    
    def filter_query(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value) |
            Q(tags__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset
    
    def filter_has_github(self, queryset, name, value):
        if value:
            return queryset.exclude(github_link='')
        return queryset

# Now let's update the views.py to use these filters:

class NotificationSettingsForm(forms.Form):
    email_on_comment = forms.BooleanField(
        required=False,
        label='Email me when someone comments on my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_follow = forms.BooleanField(
        required=False,
        label='Email me when someone follows me',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_clap = forms.BooleanField(
        required=False,
        label='Email me when someone claps for my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Profile
        fields = [
            'bio', 
            'location', 
            'website', 
            'github_username', 
            'twitter_username', 
            'avatar'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you based?'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username'
            }),
            'twitter_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Twitter username'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return avatar
