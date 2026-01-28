from .models import Course, Opinion, Urls, Slider
from academy_blog.models import Category, Article

def slider_footer(request):
    course = Course.objects.all()[:20]
    opinion = Opinion.objects.all()
    url = Urls.objects.all()
    article = Article.objects.all()[:20]

    return {
        'courses': course,
        'opinions': opinion,
        'urls': url,
        'arts': article
    }


def category(request):
    cat = Category.objects.all()
    latest_article = Article.objects.order_by('-created_at')[:10]

    return {
        'cats': cat,
        'la_ar': latest_article,
    }

def slider_image(request):
    image = Slider.objects.first()

    return {
        'slide': image,
    }