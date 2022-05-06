from django.shortcuts import render
from .models import News, Category
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator

# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import NewsSerializer
from rest_framework import status


# -----------------------Main Views--------------------------------------------
def index(request):
    searched = request.GET.get('search_word')
    if searched:
        title = 'Search Results'
        news = News.objects.filter(title__contains=searched)
        paginator = Paginator(news, 5)
        page_num = request.GET.get('page', 1)
        page_objects = paginator.get_page(page_num)
    else:
        title = 'Latest News'
        news = News.objects.all()
        paginator = Paginator(news, 5)
        page_num = request.GET.get('page', 1)
        page_objects = paginator.get_page(page_num)
    return render(request, 'news/index.html', {'title': title, 'news': news, 'page_obj': page_objects})


# -------------------------------------------------------------------------------------------------------
def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    paginator = Paginator(news, 5)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/category.html', {'news': news, 'category': category, 'page_obj': page_objects})


# -------------------------------------------------------------------------------------------------------
def read_news(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/read.html', {'news': news})


# -------------------------------------------------------------------------------------------------------
def contact_us(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_message = request.POST.get('user_message')
        if user_name and user_email and user_message:
            try:
                mail_send = send_mail(f'From {user_name}', f'{user_message}\n\nUser Email: {user_email}',
                                      settings.EMAIL_HOST_USER, ['j.ahmedov.m99@gmail.com'])
                if mail_send:
                    messages.success(request, 'Email has been successfully sent')
            except Exception as e:
                messages.error(request, 'Something went wrong')
                print(e)
    return render(request, 'news/contact.html')


# -------------------------------------------------------------------------------------------------------
def about(request):
    return render(request, 'news/about.html')


# -------------------------------------------------------------------------------------------------------
def api(request):
    return render(request, 'news/api.html')


# -----------------------API Views--------------------------------------------

class GetNewsView(APIView):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


# -------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_by_category(request, category_id):
    if request.method == 'GET':
        if category_id in range(1, 5):
            news = News.objects.filter(category_id=category_id)
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
