import traceback
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from .models import User, UserSettingsForm
from .models import PostForm, Post, Restaurant, Report
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from allauth.socialaccount.models import SocialAccount
import requests
import googlemaps
import time

from biteback import settings
import boto3
from django.urls import reverse
from django.template import loader


def get_restaurants(request):
    from biteback import settings

    if len(Restaurant.objects.all()) <= 59:
        popRestaurants()
    user = request.user
    context = {"restaurants": Restaurant.objects.all(), "user": user}
    return render(request, "restaurants.html", context)


def popRestaurants():
    from biteback import settings

    api_key = settings.GOOGLE_PLACES_API_KEY
    try:
        gmaps = googlemaps.Client(key=api_key)
        places = gmaps.places(location=(38.0335529, -78.5079772), query="restaurants")
        next_page_token = places["next_page_token"]

        # Check if places were found
        if "results" in places:
            for place in places["results"]:
                my_restaurant = Restaurant()
                my_restaurant.name = place["name"]
                my_restaurant.rating = place["rating"]
                my_restaurant.open_now = place["opening_hours"]["open_now"]
                my_restaurant.id = place["place_id"]
                my_restaurant.num_of_ratings = place["user_ratings_total"]
                my_restaurant.save()

        time.sleep(3)
        places = gmaps.places(page_token=next_page_token)
        next_page_token = places["next_page_token"]
        # Check if places were found
        if "results" in places:
            for place in places["results"]:
                my_restaurant = Restaurant()
                my_restaurant.name = place["name"]
                my_restaurant.rating = place["rating"]
                my_restaurant.open_now = place["opening_hours"]["open_now"]
                my_restaurant.id = place["place_id"]
                my_restaurant.num_of_ratings = place["user_ratings_total"]
                my_restaurant.save()

        time.sleep(3)
        places = gmaps.places(page_token=next_page_token)
        # Check if places were found
        if "results" in places:
            for place in places["results"]:
                my_restaurant = Restaurant()
                my_restaurant.name = place["name"]
                my_restaurant.rating = place["rating"]
                my_restaurant.open_now = place["opening_hours"]["open_now"]
                my_restaurant.id = place["place_id"]
                my_restaurant.num_of_ratings = place["user_ratings_total"]
                my_restaurant.save()

    except Exception as e:
        print(e)


# Create your views here.
def profile(request):
    user = request.user

    if user.is_authenticated:
        return render(request, "profile.html", {"user": user})
    return render(request, "account/login.html")


def explore(request):
    user = request.user
    return render(request, "explore.html", {"user": user})


def settings(request):

    user = request.user
    if request.method == "POST":
        # user_admin_status = request.user.is_admin
        form = UserSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            # Update user settings
            # tempAppUser.is_admin = user_admin_status
            if User.objects.filter(username=form.cleaned_data["username"]).exists() and form.cleaned_data["username"] != user.username:
                return render(request, "settings.html", {"form": form, "username_taken": True})
            user.username = form.cleaned_data["username"]
            user.save()
            # context = {'profile_photo' : str(generate_presigned_url(str(profile_photo), "download"))}
            # print(context['profile_photo'])
            return HttpResponseRedirect(
                reverse("index")
            )  # Redirect to settings page or home page ??
    else:
        initial_data = {
            "username": user.username,
            "is_admin": user.is_admin,
        }
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            # Access the user's Google profile data
            google_profile_data = social_account.extra_data
            profile_picture_url = google_profile_data.get('picture')
            form = UserSettingsForm(initial=initial_data)
            return render(request, "settings.html", {"form": form, "picture": profile_picture_url})
        else:
            form = UserSettingsForm(initial=initial_data)
            return render(request, "settings.html", {"form": form, })

            



def editprofile(request):
    user = request.user
    # new_username = UserName.username
    # user.username = new_username
    # user.save()
    return render(request, "editprofile.html", {"user": user})


def myposts(request):
    user = request.user
    user_posts = Post.objects.filter(user_id=user.id).order_by("-time_created")
    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            # Access the user's Google profile data
            google_profile_data = social_account.extra_data
            profile_picture_url = google_profile_data.get('picture')
            return render(request, "myposts.html", {"user": user, "user_posts": user_posts, "picture": profile_picture_url})
        else:
            return render(request, "myposts.html", {"user": user, "user_posts": user_posts})
    else:
        return render(request, "myposts.html", {"user": user, "user_posts": user_posts})


def report(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("post_id"):
                post = get_object_or_404(Post, pk=value)
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            # Access the user's Google profile data
            google_profile_data = social_account.extra_data
            profile_picture_url = google_profile_data.get('picture')
            return render(request, "report_block.html", {"post": post, "picture": profile_picture_url})
        else:
             return render(request, "report_block.html", {"post": post, })


def submit_report(request):
    if not request.user.is_authenticated:
        user = User.objects.filter(username="Anonymous").first()
    else:
        user = request.user
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("post_id"):
                post = get_object_or_404(Post, pk=value)
            if key.startswith("label"):
                label = value
            if key.startswith("content"):
                content = value
        report = Report(post=post, label=label, content=content, user=user)
        report.save()

    return redirect("index")


def view_reports(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("post_id"):
                post = get_object_or_404(Post, pk=value)
                reports = Report.objects.filter(post=post)

    return render(request, "report_view.html", {"post": post, "reports": reports})


def num_reports(request):
    for key, value in request.POST.items():
        if key.startswith("post_id"):
            post = get_object_or_404(Post, pk=value)

    return Report.objects.filter(post=post).__sizeof__


# Create your views here.
class profileView(generic.DetailView):
    template_name = "polls/profile.html"


def generate_presigned_url(file_name, operation):
    s3_client = boto3.client("s3")
    if operation == "upload":
        try:
            # when a user clicks the upload button the files they have attached will be stored in the s3 bucket using a
            # presigned url
            presigned_url = s3_client.generate_presigned_url(
                "put_object",
                Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": file_name},
                ExpiresIn=3600,  # URL expiration time in seconds (1 hour)
            )
        except Exception as e:
            print("Error generating presigned URL:", e)
            return None
    elif operation == "download":
        # gets presigned url to show files on main page when page loads
        try:
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": file_name},
                ExpiresIn=3600,  # URL expiration time in seconds (1 hour)
            )
        except Exception as e:
            print("Error generating presigned URL:", e)
            return None
    return presigned_url


def createpost(request):

    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # report = Post.objects.create(
            #     title=request.POST['title'],
            #     description=request.POST['description'],
            #     file=request.FILES['file']
            # )
            post = form.save(commit=False)
            # for each in User.objects.all():
            #    if each.username == "Anonymous":
            #        anonymous_user = each
            #        break
            #    else:
            #        anonymous_user = User()
            #        anonymous_user.username = "Anonymous"
            #        anonymous_user.save()
            for key, value in request.POST.items():
                if key.startswith("restaurant"):
                    restaurant = Restaurant.objects.filter(id=value).first()
            if not user.is_authenticated or "is_anonymous" in request.POST:
                anonymous_user = User.objects.filter(username="Anonymous").first()
                if not anonymous_user:
                    anonymous_user = User.objects.create_user(username="Anonymous")
                post.user = anonymous_user
                post.is_anonymous = True
            else:
                post.user = user
                post.is_anonymous = False

            post.restaurant = restaurant
            post.save()
            for file in request.FILES.getlist("files"):
                file_name = f"documents/{post.id}/{file.name}"
                presigned_url = generate_presigned_url(file_name, "upload")
                with open(file.temporary_file_path(), "rb") as data:
                    requests.put(presigned_url, data=data)
            return redirect("index")
        # return HttpResponseRedirect(reverse("index"))
    else:
        form = PostForm()

    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            # Access the user's Google profile data
            google_profile_data = social_account.extra_data
            profile_picture_url = google_profile_data.get('picture')
            return render(
                request,
                "createpost.html",
                {"form": form, "restaurants": Restaurant.objects.all(), "picture": profile_picture_url},
            )

    return render(
        request,
        "createpost.html",
        {"form": form, "restaurants": Restaurant.objects.order_by("name")},
    )


class custom_delete(DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("index")

    def delete(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get("pk")
        obj = queryset.filter(pk=pk).first()
        try:
            if obj.file:
                default_storage.delete(obj.file.name)
        except ObjectDoesNotExist:
            pass
        return obj


def main_page(request):
    '''
    try:
        restaurants = Restaurant.objects.order_by("name")
    except Exception as e:
        print("No restaurants in database, populating now...")
        popRestaurants()

    if len(Restaurant.objects.all()) <= 59:
        popRestaurants()
    print("I am at main page")
    '''
    posts = Post.objects.order_by("-time_created")
    user = request.user
    restaurants = Restaurant.objects.order_by("name")

    # for post in posts:
    #    for file in post.file.all():
    #        post.files = generate_presigned_url(f"documents/{post.id}/{file.name}", 'download')
    # print("calling render")

    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            # Access the user's Google profile data
            google_profile_data = social_account.extra_data
            profile_picture_url = google_profile_data.get('picture')
            print(profile_picture_url)
            return render(
            request,
            "index.html",
            {
                "user": user,
                "posts": posts,
                "restaurants": restaurants,
                "topics": [
                    "Out-of-Stock",
                    "Customer Service",
                    "Food Quality",
                    "Hygiene",
                    "Open/Close Status",
                    "Prices",
                    "Dining Halls",
                ],
                "picture": profile_picture_url,
            },
        )
        else :
            return render(
            request,
            "index.html",
            {
                "user": user,
                "posts": posts,
                "restaurants": restaurants,
                "topics": [
                    "Out-of-Stock",
                    "Customer Service",
                    "Food Quality",
                    "Hygiene",
                    "Open/Close Status",
                    "Prices",
                    "Dining Halls",
                ],
            },
        )
    else:
        # for post in posts:
        #    for file in post.file.all():
        #        post.files = generate_presigned_url(f"documents/{post.id}/{file.name}", 'download')
        print("calling render")
        try:
            return render(
            request,
            "index.html",
            {
                "user": user,
                "posts": posts,
                "restaurants": restaurants,
                "topics": [
                    "Out-of-Stock",
                    "Customer Service",
                    "Food Quality",
                    "Hygiene",
                    "Open/Close Status",
                    "Prices",
                    "Dining Halls",
                ],
            },
        )
        except Exception as e:
            print("an exception was thrown")
            traceback.print_exc()



# def document_view(request):
#     posts = Post.objects.all()
#     return render(request, 'document_view.html', {'posts': posts})


def anonymous_access(request):
    # Set a session variable to indicate anonymous access
    request.session["anonymous_access"] = True
    # Redirect the user to the main page or any other desired page
    return HttpResponseRedirect(reverse("index"))


def document_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            status = request.GET.get('status')
            if status:
                if status == 'new':
                    status_filter = 'New'
                elif status == 'in_progress':
                    status_filter = 'In Progress'
                elif status == 'resolved':
                    status_filter = 'Resolved'
                posts = Post.objects.filter(status=status_filter).order_by("-time_created")
            else:
                posts = Post.objects.order_by("-time_created")


            social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
            if social_account:
                # Access the user's Google profile data
                google_profile_data = social_account.extra_data
                profile_picture_url = google_profile_data.get('picture')
                return render(request, "document_view.html", {"posts": posts, "picture": profile_picture_url})

            return render(request, "document_view.html", {"posts": posts})
    return render(request, "index.html")

def post_detail(request, pk):
    if request.user.is_authenticated:
        if request.user.is_admin:
            post = get_object_or_404(Post, pk=pk)
            if (post.status == 'New'):
                post.status = 'In Progress'
                post.save()

            social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
            if social_account:
                # Access the user's Google profile data
                google_profile_data = social_account.extra_data
                profile_picture_url = google_profile_data.get('picture')
                return render(request, 'post_detail.html', {'post': post, 'picture': profile_picture_url})
            return render(request, 'post_detail.html', {'post': post})
    return render(request, "index.html")

def update_status(request, pk):
    if request.method == "POST" and request.user.is_admin:
        post = get_object_or_404(Post, pk=pk)
        new_status = request.POST.get(f'status_{pk}')
        post.status = new_status
        post.save()
        return redirect("post_detail", pk=pk) 
    return redirect("document_view")


def update_resolution_message(request, pk):
    if request.method == "POST" and request.user.is_admin:
        for key, value in request.POST.items():
            if key == "post_id":
                post_id = value
                # print(f"Post ID: {post_id}")
            if key == "resolution_message":
                resolution_message = value
                # print(f"New Status: {resolution_message}")
        post = get_object_or_404(Post, pk=post_id)
        post.resolution_message = resolution_message
        post.save()
        return redirect("post_detail", pk=pk) 
    return redirect("document_view")


def search_filter(request):
    user = request.user
    restaurants = Restaurant.objects.all()
    if request.method == "GET":
        filters = []
        topics = []
        query = 0
        for key, value in request.GET.items():
            if key.startswith("search_bar"):
                query = value
            elif key.startswith("rest_"):
                filters.append(value)
            elif key.startswith("top_"):
                topics.append(value)
        if not query and not filters and not topics:
            return clear_search(request)
        if query:
            search_results = Post.objects.filter(title__icontains=query).order_by(
                "-time_created"
            ) | Post.objects.filter(description__icontains=query).order_by(
                "-time_created"
            )
        else:
            search_results = Post.objects.order_by("-time_created")
        posts = []
        topic_posts = []
        if not topics and not filters:
            posts = search_results
        elif topics:
            for topic in topics:
                topic_posts.extend(search_results.filter(topic=topic))
            if filters:
                for _filter in filters:
                    for post in topic_posts:

                        if post.restaurant.id == _filter:
                            posts.append(post)
            else:
                posts = topic_posts
        elif filters:
            for _filter in filters:
                posts.extend(search_results.filter(restaurant=_filter))
        if user.is_authenticated:
            social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
            if social_account:
                # Access the user's Google profile data
                google_profile_data = social_account.extra_data
                profile_picture_url = google_profile_data.get('picture')
                print(profile_picture_url)
                return render(
                    request,
                    "index.html",
                    {
                        "user": user,
                        "posts": posts,
                        "restaurants": restaurants,
                        "search_query": query,
                        "filters": filters,
                        "topics": [
                            "Out-of-Stock",
                            "Customer Service",
                            "Food Quality",
                            "Hygiene",
                            "Open/Close Status",
                            "Prices",
                            "Dining Halls",
                        ],
                        "topic_filters": topics,
                        "picture": profile_picture_url,
                    },
                )
        else:
            return render(
                request,
                "index.html",
                {
                    "user": user,
                    "posts": posts,
                    "restaurants": restaurants,
                    "search_query": query,
                    "filters": filters,
                    "topics": [
                        "Out-of-Stock",
                        "Customer Service",
                        "Food Quality",
                        "Hygiene",
                        "Open/Close Status",
                        "Prices",
                        "Dining Halls",
                    ],
                    "topic_filters": topics,
                }
            )



def clear_search(request):
    return redirect("index")
