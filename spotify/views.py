#  Description: Music Monolith Marketing Website
#  Author: Benjamin Orrvick
#  Author URL:  https://github.com/borrvick/
#  Purpose: create a spotify object and return query reseults and display to webpage
#  Tags: Music, Marketing, Business, Website, Application

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .base_api_class import SpotifyAPI
from .playlistObjects import playlistObjects
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import csv
from django.conf import settings
from .models import CSVFile
import json
import datetime
from django.core.files.storage import default_storage


def home(request):
    return render(request, "spotify/home.html", {"title": "Home"})


@login_required
def search(request):
    return render(request, "spotify/search.html", {"title": "Search"})


def how(request):
    return render(request, "spotify/how.html", {"title": "How to Use"})


def faq(request):
    return render(request, "spotify/faq.html", {"title": "FAQ's"})


def searchAndCreateJson(
    request, spotify, query, search_type, CONST_LIMIT, offset, searchObjList
):
    spotifyJsonData = spotify.search(query, search_type, CONST_LIMIT, offset)
    return convertJsonToList(request, spotifyJsonData, searchObjList)


# adds the json object contents to a list so we can have access to the entire search at once
def convertJsonToList(request, spotifyJsonData, searchObjList):
    # sometimes spoitfy API returns incomplete data or "None" for some attributes. Trying search again fixes issue
    try:
        # for each item in the dictionary add it to the playlist list
        for item in spotifyJsonData["playlists"]["items"]:
            # appends each search to the playlist to create a lsit of max 1000 since thats all the more search results allowed
            tempPlaylist = playlistObjects(
                item["name"],
                item["description"],
                item["external_urls"]["spotify"],
                item["owner"]["display_name"],
                item["owner"]["external_urls"]["spotify"],
            )
            # we only want playlist if there is a contact. Thats why were create a list and have a class in the first place
            if tempPlaylist.email != "None" or tempPlaylist.insta != "None":
                searchObjList.append(tempPlaylist)
        return searchObjList

    except Exception:
        print("Search Failed. Try Again.")


def createPagination(request, object):
    paginator = Paginator(object, 10)
    try:
        page = int(request.GET.get("page", 1))
    except Exception:
        page = 1
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    return lists


# creates a csv of playlists to be used when sending emails and stored in db
def createPlaylistCSV(request, searchObjList, query, profile):
    # the filename is specific to store in media folder AND database and has time included so file duplicated does not happen
    file_name = f"spotify_csv/{profile}/{query}_{datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S')}.csv"
    file = default_storage.open(file_name, "w")
    csvWriter = csv.writer(file)

    csvWriter.writerow(
        [
            "Playlist Name",
            "Playlist Description",
            "Playlist Url",
            "Username",
            "Profile Url",
            "Email",
            "Instagram",
        ]
    )

    for x in searchObjList:
        csvWriter.writerow(
            [
                x.playlistName,
                x.playlistDescription,
                x.playlistUrl,
                x.profile,
                x.profileUrl,
                x.email,
                x.insta,
            ]
        )
    file.write(csvWriter)
    file.close()

    savePlaylistCSV(request, query, file_name, profile)


def deletePlaylistCSV(request, profile):
    CSVFile.objects.filter(profile=profile).earliest("created_at").delete()


# i got the new created file to save to s3 now all i have to do is located it and save it to the db bb
# make sure they delete when they are supposed to and we are good!!!!
def savePlaylistCSV(request, query, file, profile):
    # # # delete the oldest search so we onl have most recent 5
    if CSVFile.objects.filter(profile=profile).count() == 5:
        deletePlaylistCSV(request, profile)

    newCSV = CSVFile.objects.create(
        id=None, profile=profile, name=query, csv=file
    )
    newCSV.save()


def createSearchResults(request):

    query = request.GET.get("q")

    if not request.GET.get("page"):
        if request.method == "GET":
            profile = request.user.profile
            # search parameter. This will eventually be a value returned from user input textbox
            search_type = "playlist"
            CONST_LIMIT = (
                50  # ~50 is the max search at a time allowed by spotify
            )
            offset = 0
            CONST_OFFSET_LIMIT = 1000  # 1000 is max spotify allows
            # create a list to add all the json objects that are searched to
            searchObjList = []
            spotify = SpotifyAPI(settings.CLIENT_ID, settings.CLIENT_SECRET)

            # since not every playlist will have the data we want, we want to run it as many times as allowed so we have enough
            # data to show the user
            # offset starts at 0 and goes to 1000 which is the limit spotify allows
            while offset < CONST_OFFSET_LIMIT:

                searchAndCreateJson(
                    request,
                    spotify,
                    query,
                    search_type,
                    CONST_LIMIT,
                    offset,
                    searchObjList,
                )
                # increase the search paremeter to get the next 50 results
                offset += 50

            # if search returned results create a csv file of resutls
            if searchObjList:
                createPlaylistCSV(request, searchObjList, query, profile)
            # convert lit to json object then dictionary to store as session
            json_string = json.dumps([ob.__dict__ for ob in searchObjList])
            json_dict = json.loads(json_string)
            request.session["playlists"] = json_dict
            # using session to store searches so we can paginate them and not lose them
            context = {
                "PlaylistList": createPagination(
                    request, request.session["playlists"]
                ),
                "searchquery": query,
            }

        # if it didnt work send an empty list
        else:
            context = {
                "PlaylistList": "",
                "searchquery": "",
            }

    else:
        # if search already happened just pass the session object to use pagination
        context = {
            "PlaylistList": createPagination(
                request, request.session["playlists"]
            ),
            "searchquery": query,
        }

    return render(request, "spotify/results.html", context)
