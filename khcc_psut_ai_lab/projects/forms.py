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
    Solution,
    Team
)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from khcc_psut_ai_lab.constants import TALENT_TYPES



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
        label='Email me when someone clap_count for my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
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
        fields = [
            'title', 'description', 'github_link', 'tags',
            'pdf_file', 'featured_image', 'additional_files',
            'youtube_url', 'is_gold', 'token_reward',
            'gold_goal', 'deadline'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'tags': forms.TextInput(
                attrs={'placeholder': 'Enter tags separated by commas'}
            ),
            'gold_goal': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # Only show gold seed fields to faculty members
        if self.user and not self.user.groups.filter(name='Faculty').exists():
            self.fields.pop('is_gold', None)
            self.fields.pop('token_reward', None)
            self.fields.pop('gold_goal', None)
            self.fields.pop('deadline', None)
        else:
            # Add help text for faculty members
            self.fields['is_gold'].help_text = "Mark this as a Gold Seed to offer tokens for completion"
            self.fields['token_reward'].help_text = "Number of tokens to award for completion"
            self.fields['gold_goal'].help_text = "How tokens will be awarded"
            self.fields['deadline'].help_text = "Deadline for submitting solutions"
            
            # If this is an existing project, format the deadline
            if instance and instance.deadline:
                self.initial['deadline'] = instance.deadline.strftime('%Y-%m-%dT%H:%M')

    def clean_github_link(self):
        """Validate GitHub repository URL"""
        url = self.cleaned_data['github_link']
        if url:  # Only validate if URL is provided
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
        
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
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
            if pdf_file.size > 10 * 1024 * 1024:
                raise ValidationError('PDF file must be smaller than 10MB')

            ext = os.path.splitext(pdf_file.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError('Only PDF files are allowed')

            file_type, encoding = mimetypes.guess_type(pdf_file.name)
            if file_type != 'application/pdf':
                raise ValidationError('Invalid PDF file')

        return pdf_file

    def clean_featured_image(self):
        """Validate and process featured image"""
        image = self.cleaned_data.get('featured_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 5MB')

            try:
                img = Image.open(image)
                
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                if img.width > 2000 or img.height > 2000:
                    raise ValidationError('Image dimensions should not exceed 2000x2000 pixels')
                
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
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
    """Form for adding comments to projects"""
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

# Add this class to forms.py

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
        model = UserProfile
        fields = [
            'avatar',
            'bio',
            'location',
            'website',
            'github_username',
            'linkedin_url',
            'title',
            'department',
            'research_interests',
            
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
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your LinkedIn URL'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']

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
    query = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-clap_count', 'Most popular'),
            ('title', 'Alphabetical'),
        ]
    )

class AdvancedSearchForm(forms.Form):
    """Advanced search form"""
    query = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    min_claps = forms.IntegerField(required=False, min_value=0)
    has_github = forms.BooleanField(required=False)
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-clap_count', 'Most popular'),
            ('-comment_count', 'Most discussed'),
            ('title', 'Alphabetical'),
            ('-rating_avg', 'Highest rated')
        ]
    )


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

class ProjectForm(forms.ModelForm, FileValidationMixin):
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
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project in detail...'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repository'
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
        url = self.cleaned_data['github_link']
        if url:  # Only validate if URL is provided
            if not url.startswith(('https://github.com/', 'http://github.com/')):
                raise ValidationError('Please enter a valid GitHub repository URL')
            
            try:
                URLValidator()(url)
            except ValidationError:
                raise ValidationError('Please enter a valid URL')
        
        return url

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            return ''
        
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        seen = set()
        unique_tags = [x for x in tag_list if not (x in seen or seen.add(x))]
        
        if len(unique_tags) > 5:
            raise ValidationError('Please enter no more than 5 unique tags')
        
        if any(len(tag) > 20 for tag in unique_tags):
            raise ValidationError('Each tag must be less than 20 characters')
        
        return ', '.join(unique_tags)

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            self.validate_file_size(pdf_file, 10)
            self.validate_file_type(pdf_file, ['application/pdf'])
        return pdf_file

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            self.validate_file_size(image, 5)
            img = self.validate_image(image)
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            if img.width > 1200 or img.height > 1200:
                output_size = (1200, 1200)
                img.thumbnail(output_size, Image.LANCZOS)
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            from django.core.files.uploadedfile import InMemoryUploadedFile
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{os.path.splitext(image.name)[0]}.jpg",
                'image/jpeg',
                output.tell(),
                None
            )
        return image

class CommentForm(forms.ModelForm, FileValidationMixin):
    """Form for adding comments to projects"""
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) < 10:
            raise ValidationError('Comment must be at least 10 characters long')
        if len(content) > 1000:
            raise ValidationError('Comment must be less than 1000 characters')
        return content

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            self.validate_file_size(image, 2)
            img = self.validate_image(image, 1000)
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            if img.width > 800 or img.height > 800:
                output_size = (800, 800)
                img.thumbnail(output_size, Image.LANCZOS)
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            from django.core.files.uploadedfile import InMemoryUploadedFile
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{os.path.splitext(image.name)[0]}.jpg",
                'image/jpeg',
                output.tell(),
                None
            )
        return image

class UserProfileForm(forms.ModelForm, FileValidationMixin):
    """Form for user profile management"""
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'website', 'github_username',
            'linkedin_url', 'avatar', 'email_on_comment',
            'email_on_follow', 'email_on_clap', 'email_on_bookmark'
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
                'placeholder': 'https://yourwebsite.com'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/your-profile'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            self.validate_file_size(avatar, 5)
            img = self.validate_image(avatar)
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
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
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.Select(attrs={
                'class': 'form-select'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your review here...'
            })
        }

class BookmarkForm(forms.ModelForm):
    """Form for managing bookmarks"""
    class Meta:
        model = Bookmark
        fields = ['project']
        widgets = {
            'project': forms.HiddenInput()
        }

class NotificationSettingsForm(forms.Form):
    """Form for notification preferences"""
    email_on_comment = forms.BooleanField(
        required=False,
        label='Email me when someone comments on my projects'
    )
    email_on_follow = forms.BooleanField(
        required=False,
        label='Email me when someone follows me'
    )
    email_on_clap = forms.BooleanField(
        required=False,
        label='Email me when someone clap_count for my projects'
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects'
    )

class ProjectSearchForm(forms.Form):
    """Form for project search and filtering"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search seeds...'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by tags (comma separated)'
        })
    )
    
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-clap_count', 'Most popular'),
            ('title', 'Alphabetical'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

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
            ('-clap_count', 'Most popular'),
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
    

# In forms.py
from django import forms
from .models import Project, Comment
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
import os

class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""
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
        fields = ['title', 'description', 'github_link', 'tags', 'youtube_url', 
                 'pdf_file', 'featured_image', 'additional_files']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show gold seed fields to faculty members
        if self.user and self.user.groups.filter(name='Faculty').exists():
            self.fields['is_gold'] = forms.BooleanField(required=False)
            self.fields['token_reward'] = forms.IntegerField(required=False)
            self.fields['gold_goal'] = forms.ChoiceField(
                choices=[
                    ('all', 'All Complete'),
                    ('first', 'First to Complete'),
                    ('best', 'Best Solution')
                ],
                required=False
            )
            self.fields['deadline'] = forms.DateTimeField(
                required=False,
                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
            )
        
    def clean_youtube_url(self):
        url = self.cleaned_data.get('youtube_url')
        if url:
            from .models import validate_youtube_url
            validate_youtube_url(url)
        return url

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file and pdf_file.size > 10 * 1024 * 1024:  # 10MB limit
            raise ValidationError('PDF file must be smaller than 10MB')
        return pdf_file

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image file must be smaller than 5MB')
            try:
                img = Image.open(image)
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Resize if needed
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85)
                output.seek(0)
                
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

class ExtendedUserCreationForm(UserCreationForm):
    talent_type = forms.ChoiceField(
        choices=TALENT_TYPES,
        required=True,
        label='Select Your Talent Type',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'talent_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                talent_type=self.cleaned_data['talent_type']
            )
        return user

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['content', 'files', 'github_link']

from django import forms
from .models import Team, TeamDiscussion, TeamComment, TeamMembership

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'tags', 'team_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your team and its goals'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., AI, Healthcare, Research)'
            }),
            'team_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.instance.pk:
            if Team.objects.exclude(pk=self.instance.pk).filter(name__iexact=name).exists():
                raise forms.ValidationError('A team with this name already exists.')
        else:
            if Team.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError('A team with this name already exists.')
        return name

class TeamDiscussionForm(forms.ModelForm):
    class Meta:
        model = TeamDiscussion
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6})
        }

class TeamCommentForm(forms.ModelForm):
    class Meta:
        model = TeamComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }

class TeamMembershipForm(forms.ModelForm):
    class Meta:
        model = TeamMembership
        fields = ['role', 'is_approved']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow certain role choices based on permissions
        user = kwargs.get('initial', {}).get('user')
        if user and not user.is_staff:
            self.fields['role'].choices = [
                ('member', 'Member'),
                ('moderator', 'Moderator')
            ]

class TeamNotificationSettingsForm(forms.Form):
    email_notifications = forms.BooleanField(required=False)
    in_app_notifications = forms.BooleanField(required=False)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'tags', 'team_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Enter tags separated by commas'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Team.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A team with this name already exists.')
        return name
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            # Split tags by comma and clean them
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            # Rejoin cleaned tags
            return ', '.join(tag_list)
        return tags