from django.shortcuts import HttpResponse

def items(request):
    return HttpResponse("Item 1 is Raspberry Pi.")