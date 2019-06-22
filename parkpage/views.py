from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import AlertItem, CenterItem, LessonItem
import urllib.request, json

#Sets up initial page when link to a park is clicked on
def parkpageView (request, park_code):
    park_name = getParkName (park_code)
    park_desc = getParkDesc (park_code)
    return render (request, 'parkpage.html',{'parkName': park_name, 'parkCode': park_code, 'parkDescription': park_desc})

#Get name of park given park code
def getParkName (park_code):
    return getParkQuality (park_code, "fullName")

#Get description of park given park code
def getParkDesc (park_code):
    return getParkQuality (park_code, "description")

# Gets the quality q of a park
def getParkQuality (park_code, q):
    search_term = park_code.lower()
    api_key = "WPAswbcCtp3pwn2LhRNIcasP14NJiyxAjis6Abdm"
    endpoint = "https://developer.nps.gov/api/v1/parks?parkCode=" + park_code + "&api_key=" + api_key
    req = urllib.request.Request(endpoint,headers={"Authorizaton": api_key})
    response = urllib.request.urlopen(req).read()
    data = json.loads(response.decode('utf-8'))
    list_length = len(data)
    return data["data"][0][q]

#Sets up page to display alerts for a given park
def alertsView (request, park_code):
    #Clear any old alerts
    for r in AlertItem.objects.all():
       (AlertItem.objects.get(id=r.id)).delete()

    #Generate new alerts
    alert_list = get_alert_title_desc_url(park_code)
    for i in range(len(alert_list)):
        new_item_in_list = AlertItem (title = alert_list[i][0],
                                    desc = alert_list[i][1],
                                    url = alert_list[i][2])
        new_item_in_list.save()
    alerts = AlertItem.objects.all()

    #Get park name
    park_name = getParkName (park_code)

    #Tells how many alerts there are
    num_rs = "There are " + str(len(alert_list)) + " alert(s) "

    #Render alertpage.html with all_alerts and parkName
    return render (request, 'alertpage.html',
                  {'all_alerts': alerts, 'parkName': park_name, 'numResults': num_rs})

#Helper for alertsView
# return list of lists of length 3 holding title, description, and url of each alert
def get_alert_title_desc_url(park_code):
	#jason: json object fm nps api
    api_key = "zzoRoOUg0Gv5rrHFPfZVsaHSsIjGO8OieJNY8mig"
    endpoint = "https://developer.nps.gov/api/v1/alerts?parkCode=" + park_code + "&api_key=" + api_key
    req = urllib.request.Request(endpoint,headers={"Authorizaton": api_key})
    response = urllib.request.urlopen(req).read()
    jason = json.loads(response.decode('utf-8'))

    alert_list = jason["data"]
    for i in range(len(alert_list)):
        alert_list[i] = [jason["data"][i]["category"] + ": " + jason["data"][i]["title"],
                        jason["data"][i]["description"],
                        jason["data"][i]["url"]]

    return alert_list

#Sets up page to display visitor centers for a given park
def visitorView (request, park_code):
        #Clear any old centers
        for r in CenterItem.objects.all():
           (CenterItem.objects.get(id=r.id)).delete()

        #Generate new centers
        center_list = get_centers_name_desc_dir(park_code)
        for i in range(len(center_list)):
            new_item_in_list = CenterItem (name = center_list[i][0],
                                        desc = center_list[i][1],
                                        dir = center_list[i][2])
            new_item_in_list.save()
        centers = CenterItem.objects.all()

        #Get park name
        park_name = getParkName (park_code)

        #Tells how many visitor centers there are
        num_rs = "There are " + str(len(center_list)) + " visitor center(s) "

        #Render alertpage.html with all_centers and parkName
        return render (request, 'visitorpage.html',
                      {'all_centers': centers, 'parkName': park_name, 'numResults': num_rs})

#Helper for visitorView
# return list of lists of length 3 holding name, description, and directions of each alert
def get_centers_name_desc_dir(park_code):
	return get_generic("visitorcenters", park_code, "name", "description", "directionsInfo")

#Sets up page to display 'Learn More!' page for a given park
def learnView (request, park_code):
    park_name = getParkName (park_code)
    return render (request, 'learnpage.html', {'parkCode': park_code, 'parkName': park_name})

#Sets up page to display 'Events' page for a given park
def eventView (request, park_code):
    #Clear any old events
    for r in LessonItem.objects.all():
       (LessonItem.objects.get(id=r.id)).delete()

    #Generate new events
    item_list = get_generic("events", park_code, "title", "description", "url")
    for i in range(len(item_list)):
        desc = (item_list[i][1]).replace("<p>","")
        desc1 = desc.replace("</p>","")
        desc = desc1.replace("<em>","")
        desc1 = desc.replace("</em>","")
        desc = desc1.replace("<br/>","")
        new_item_in_list = LessonItem (title = item_list[i][0],
                                    q2 = desc,
                                    url = "")
        new_item_in_list.save()
    item_models = LessonItem.objects.all()

    #Get park name
    title = "There are " + str(len(item_list)) + " events(s) at " + (getParkName (park_code)) + ": "

    #Render eventpage.html with all_items and parkName
    return render (request, 'eventpage.html',
                  {'all_items': item_models, 'title': title, 'q2':"Description"})

#Sets up page to display 'Campgrounds' page for a given park
def campgroundView (request, park_code):
    #Clear any old campgrounds
    for r in LessonItem.objects.all():
       (LessonItem.objects.get(id=r.id)).delete()

    #Generate new campgrounds
    item_list = get_generic("campgrounds", park_code, "name", "id", "id")
    for i in range(len(item_list)):
        new_item_in_list = LessonItem (title = item_list[i][0],
                                    q2 = item_list[i][1],
                                    url = item_list[i][2])
        new_item_in_list.save()
    item_models = LessonItem.objects.all()

    #Get park name
    title = "There are " + str(len(item_list)) + " campground(s) for " + (getParkName (park_code)) + ": "

    #Render eventpage.html with all_alerts and parkName
    return render (request, 'eventpage.html',
                  {'all_items': item_models, 'title': title, 'q2':"Campground Identification String:"})

#Sets up page to display 'Lessons Plans' page, within 'Learn More', for a given park
def lessonView (request, park_code):
        #Clear any old lessons
        for r in LessonItem.objects.all():
           (LessonItem.objects.get(id=r.id)).delete()

        #Generate new lessons
        item_list = get_lesson_title_grade_url(park_code)
        for i in range(len(item_list)):
            new_item_in_list = LessonItem (title = item_list[i][0],
                                        q2 = item_list[i][1],
                                        url = item_list[i][2])
            new_item_in_list.save()
        item_models = LessonItem.objects.all()

        #Get park name
        title = "There are " + str(len(item_list)) + " lesson(s) for " + (getParkName (park_code)) + ": "

        #Render genericpage.html with all_lessons and parkName
        return render (request, 'genericpage.html',
                      {'all_items': item_models, 'title': title, 'q2':"Duration: "})

#Helper for lessonView
# return list of lists of length 3 holding title, grade, and url of each news release
def get_lesson_title_grade_url(park_code):
	return get_generic("lessonplans", park_code, "title", "duration", "url")

#Sets up page to display 'News Releases', within 'Learn More!' for a given park
def newsView (request, park_code):
        #Clear any old news
        for r in LessonItem.objects.all():
           (LessonItem.objects.get(id=r.id)).delete()

        #Generate new news
        item_list = get_news_title_date_url(park_code)
        for i in range(len(item_list)):
            new_item_in_list = LessonItem (title = item_list[i][0],
                                        q2 = item_list[i][1],
                                        url = item_list[i][2])
            new_item_in_list.save()
        item_models = LessonItem.objects.all()

        #Get park name
        title = "There are " + str(len(item_list)) + " news release(s) for " + (getParkName (park_code)) + ": "

        #Render genericpage.html with all_items and parkName
        return render (request, 'genericpage.html',
                      {'all_items': item_models, 'title': title, 'q2':"Abstract: "})

#Helper for newsView
# return list of lists of length 3 holding title, date, and url of each news release
def get_news_title_date_url(park_code):
	return get_generic("newsreleases", park_code, "title", "abstract", "url")

#Sets up page to display 'Articles' within 'Learn More' for a given park
def articleView (request, park_code):
        #Clear any old articles
        for r in LessonItem.objects.all():
           (LessonItem.objects.get(id=r.id)).delete()

        #Generate new articles
        item_list = get_article_title_desc_url(park_code)
        for i in range(len(item_list)):
            new_item_in_list = LessonItem (title = item_list[i][0],
                                        q2 = "",
                                        url = item_list[i][2])
            new_item_in_list.save()
        item_models = LessonItem.objects.all()

        #Get park name
        title = "There are " + str(len(item_list)) + " article(s) for " + (getParkName (park_code)) + ": "

        #Render egenricpage.html with all_items and parkName
        return render (request, 'genericpage.html',
                      {'all_items': item_models, 'title': title, 'q2':""})

#Helper for articleView
# return list of lists of length 3 holding title, description, and url of each news release
def get_article_title_desc_url(park_code):
	return get_generic("articles", park_code, "title", "title", "url")

#Sets up page to display 'People' within 'Learn More' for a given park
def peopleView (request, park_code):
        #Clear any old people
        for r in LessonItem.objects.all():
           (LessonItem.objects.get(id=r.id)).delete()

        #Generate new people
        item_list = get_people_name_desc_url(park_code)
        for i in range(len(item_list)):
            new_item_in_list = LessonItem (title = item_list[i][0],
                                        q2 = "",
                                        url = item_list[i][2])
            new_item_in_list.save()
        item_models = LessonItem.objects.all()

        #Get park name
        title = "There are " + str(len(item_list)) + " person(s) from " + (getParkName (park_code)) + ": "

        #Render genericpage.html with all_items and parkName
        return render (request, 'genericpage.html',
                      {'all_items': item_models, 'title': title, 'q2':""})

#Helper for peopleView
# return list of lists of length 3 holding name, description, and url of each news release
def get_people_name_desc_url(park_code):
    return get_generic("people", park_code, "title", "title", "url")

#Sets up page to display 'Places' within 'Learn More' for a given park
def placeView (request, park_code):
        #Clear any old places
        for r in LessonItem.objects.all():
           (LessonItem.objects.get(id=r.id)).delete()

        #Generate new places
        item_list = get_place_name_desc_url(park_code)
        for i in range(len(item_list)):
            new_item_in_list = LessonItem (title = item_list[i][0],
                                        q2 = "",
                                        url = item_list[i][2])
            new_item_in_list.save()
        item_models = LessonItem.objects.all()

        #Get park name
        title = "There are " + str(len(item_list)) + " place(s) for " + (getParkName (park_code)) + ": "
        #Render genericpage.html with all_items and parkName
        return render (request, 'genericpage.html',
                      {'all_items': item_models, 'title': title, 'q2':""})

#Helper for placeView
# return list of lists of length 3 holding name, description, and url of each news release
def get_place_name_desc_url(park_code):
    return get_generic("places", park_code, "title", "url", "url")

#Helper to get 3 qualities q1, q2, q3 from park item obtained from 'category'
def get_generic(category, park_code, q1, q2, q3):#jason: json object fm nps api
    api_key = "zzoRoOUg0Gv5rrHFPfZVsaHSsIjGO8OieJNY8mig"
    endpoint = "https://developer.nps.gov/api/v1/" + category + "?parkCode=" + park_code + "&api_key=" + api_key
    req = urllib.request.Request(endpoint,headers={"Authorizaton": api_key})
    response = urllib.request.urlopen(req).read()
    jason = json.loads(response.decode('utf-8'))

    item_list = jason["data"]
    for i in range(len(item_list)):
        ins2 = "none available"
        ins3 = "none available"
        if q2 in jason["data"][i]:
            ins2 = jason["data"][i][q2]
        if q3 in jason["data"][i]:
            ins3 = jason["data"][i][q3]
        item_list[i] = [jason["data"][i][q1],ins2,ins3]
    return item_list
