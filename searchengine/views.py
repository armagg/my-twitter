from django.shortcuts import render

# Create your views here.
from searchengine.models import DocIndex


def search(request):
    if request.POST:
        words = str(request.POST.get('words')).split(' ')
        results = []
        print('words')
        print(words)
        for word in words:
            print('word')
            print(word)
            for result in DocIndex.search(word):
                print('result')
                print(result)
                results.append(result)
        print('results')
        print(results)
        return render(request, 'searchengin/search.html', {'results': results})
    else:
        return render(request, 'searchengin/search.html')
