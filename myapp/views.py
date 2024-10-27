from django.http import HttpResponse

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def about(request):
    return HttpResponse('About')