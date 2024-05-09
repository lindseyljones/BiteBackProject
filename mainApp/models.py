from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from biteback import settings
from django.utils import timezone

# Create your models here.


class Search(models.Model):
    search = models.CharField(max_length=50, default="")


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ["search"]


class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="")
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    id = models.CharField(max_length=200, default="", primary_key=True)
    open_now = models.BooleanField("open status", default=True)
    num_of_ratings = models.IntegerField()


class UserSettingsForm(forms.Form):
    """
    STATUS_CHOICES = []
    for each in Restaurant.objects.all():
        STATUS_CHOICES.append((each.name, each.name))
    STATUS_CHOICES = tuple(STATUS_CHOICES)
    favorite_restaurant_1 = forms.ChoiceField(
        label='Favorite Restaurant 1',
        choices=STATUS_CHOICES,
        widget=Select2Widget(),
        required=False
    )
    favorite_restaurant_2 = forms.ChoiceField(
        label='Favorite Restaurant 2',
        choices=STATUS_CHOICES,
        widget=Select2Widget(),
        required=False
    )
    favorite_restaurant_3 = forms.ChoiceField(
        label='Favorite Restaurant 3',
        choices=STATUS_CHOICES,
        widget=Select2Widget(),
        required=False
    )
    """

    username = forms.CharField(label="Username", max_length=100)

    # Define the fields with forms.ChoiceField and use the Select2Widget for searchable dropdown


class User(AbstractUser):
    is_admin = models.BooleanField("admin status", default=False)
    has_profile_photo = models.BooleanField(
        "User's profile photo status", default=False
    )
    # favorite_restaurant_3 = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)
    # favorite_restaurant_2 = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)
    # favorite_restaurant_1 = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)


class Post(models.Model):

    STATUS_CHOICES = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    )

    TOPICS = (
        ("Out-of-Stock", "Out-of-Stock"),
        ("Customer Service", "Customer Service"),
        ("Food Quality", "Food Quality"),
        ("Hygiene", "Hygiene"),
        ("Open/Close Status", "Open/Close Status"),
        ("Prices", "Prices"),
        ("Dining Halls", "Dining Halls"),
    )

    title = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    file = models.FileField(upload_to="documents/%Y/%m/%d", default=None, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    resolution_message = models.CharField(
        max_length=40, default="Problem Has Been Resolved"
    )
    time_created = models.DateTimeField(default=timezone.now)
    is_anonymous = models.BooleanField("anonymous status", default=False)
    topic = models.CharField(max_length=40, choices=TOPICS, default="Topic")
    restaurant = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)


class Report(models.Model):

    REPORT_LABELS = (
        ("Inaccurate", "Inaccurate"),
        ("Problem is Resolved", "Problem is Resolved"),
    )

    post = models.ForeignKey(Post, default=1, on_delete=models.CASCADE)
    label = models.CharField(max_length=40, choices=REPORT_LABELS, default="Inaccurate")
    content = models.TextField(default="")
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)


class PostForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(required=False, initial=False)

    file = forms.FileField(
        label="Select a file",
        help_text="max. 2 megabytes",
        required=False,
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "file",
            "status",
            "is_anonymous",
            "topic",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title... (max 100 characters)",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Type something...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Hide the status field in the form
        self.fields["status"].widget = forms.HiddenInput()
        self.fields["topic"].strip = False

    def save(self, commit=True):
        # Force status to be 'New' when creating a new post
        self.instance.status = "New"
        return super().save(commit)
