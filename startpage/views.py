
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ResultItem
import urllib.request, json

#Initial start page, user not yet chosen whether to search by state or park code
def startpageView (request):
    all_result_items = ResultItem.objects.all()
    return render (request, 'startpagechoose.html',
                  {'search_results': all_result_items})
#Start page, user chose to search by state
def startstateView (request):
    all_result_items = ResultItem.objects.all()
    return render (request, 'startpagestate.html',
                  {'search_results': all_result_items})
#Start page, user chose to search by park code
def startparkView (request):
    all_result_items = ResultItem.objects.all()
    return render (request, 'startpagepark.html',
                  {'search_results': all_result_items})

#Populates start page with search results from searching by park code
def searchParks2 (request, search_term):
    for r in ResultItem.objects.all():
       (ResultItem.objects.get(id=r.id)).delete()

    results = getSearchResults (search_term)
    for i in range(len(results[0])):
        new_item_in_list = ResultItem (content = results[0][i], parkcode = results[1][i])
        new_item_in_list.save()

    #this will reload page at /start/
    return HttpResponseRedirect ('/start/')

#Populates start page with search results from searching by state
def searchParks (request):
    # search_term = request.POST ['search_term']
    # results = getSearchResults (search_term)
    #
    #in request, find attribute with this name
     for r in ResultItem.objects.all():
        (ResultItem.objects.get(id=r.id)).delete()

     search_term = request.POST ['search_term']
     results = getSearchResults (search_term)

     for i in range(len(results[0])):
         new_item_in_list = ResultItem (content = results[0][i], parkcode = results[1][i])
         new_item_in_list.save()

     #this will reload page at /start/
     return HttpResponseRedirect ('/start/')

def setUpParkView (request, park_code):
    for r in ResultItem.objects.all():
        (ResultItem.objects.get(id=r.id)).delete()
    return HttpResponseRedirect('/park/' + park_code)

#REturns list of tuples of name and prk code for each park search result
def getSearchResults (search_term):
    r1 = getSearchResultsHelper ("parks?stateCode=", search_term)
    r2 = getSearchResultsHelper ("parks?parkCode=", search_term)
	#	r3 = filterByName (mapToName (getSearchResultsHelper ("parks?limit=", "600")), search_term)
    results = []
    results.extend (r1)
    results.extend (r2)
    return [mapToName (results), mapToCode (results)]
    #return results

#returns list of park item objects
def getSearchResultsHelper (param, search_term):
    search_term = search_term.lower()
    api_key = "WPAswbcCtp3pwn2LhRNIcasP14NJiyxAjis6Abdm"
    endpoint = "https://developer.nps.gov/api/v1/" + param + search_term + "&api_key=" + api_key
    req = urllib.request.Request(endpoint,headers={"Authorizaton": api_key})
    response = urllib.request.urlopen(req).read()
    data = json.loads(response.decode('utf-8'))
    list_length = len(data)
    return data["data"]

#Given list of park objects map to list of their names
def mapToName (L):
    newL = ["" for x in range (len(L))]
    for i in range(len(L)):
        newL[i] = L[i]["fullName"]
    return newL
#Given list of park objects map to list of their park codes
def mapToCode (L):
    newL = ["" for x in range (len(L))]
    for i in range(len(L)):
        newL[i] = L[i]["parkCode"]
    return newL
