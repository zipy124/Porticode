from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, Queue
import spotipy
import spotipy.util as util
from background_task import background
from random import randint
from django.contrib.admin.views.decorators import staff_member_required

CURRENTLY_PLAYING_SONG = None

def index(request):
    if(not request.user.is_authenticated()):
        return redirect('auth_ucl:student_login')
    locations = Location.objects.all()
    context = {
        "locations": locations
    }
    return render(request, 'music/locations.html', context)

def location(request, location_id):
    if(not request.user.is_authenticated()):
        return redirect('auth_ucl:student_login')
    location = get_object_or_404(Location, pk=location_id)
    current_queue = Queue.objects.all().filter(location=location_id).order_by('-votes')
    context = {
        'location': location,
        'queue': current_queue,
    }
    return render(request, 'music/location.html', context)

def song_request(request, location_id):
    if(not request.user.is_authenticated()):
        return redirect('auth_ucl:student_login')
    location = get_object_or_404(Location, pk=location_id)
    context = {
        'location': location,
    }
    return render(request, 'music/request.html', context)

def song_list(request, location_id):
    if(not request.user.is_authenticated()):
        return redirect('auth_ucl:student_login')
    location = get_object_or_404(Location, pk=location_id)
    song_name = request.GET.get("song_name", "")

    token = util.oauth2.SpotifyClientCredentials(client_id=location.spotipy_client_id, client_secret=location.spotipy_client_secret)
    cache_token = token.get_access_token()
    spotify = spotipy.Spotify(cache_token)

    songs = spotify.search(q=song_name, type="track", limit=10)['tracks']['items']

    context = {
        'location': location,
        'songs': songs
    }
    return render(request, 'music/list.html', context)

def add_song(request, location_id):
    if(not request.user.is_authenticated()):
        return redirect('auth_ucl:student_login')
    location = get_object_or_404(Location, pk=location_id)
    song_uri = request.GET.get("song_uri", "")
    song_name = request.GET.get("song_name", "")
    song_artist = request.GET.get("song_artist", "")
    song = Queue.objects.get_or_create(song_URI=song_uri, song_name=song_name, song_artist=song_artist, location=location)[0]
    song.votes += 1
    song.save()

    return redirect('music:location', location_id)

def now_playing(request, location_id):
    if(not request.user.is_authenticated()):
        return redirect('auth_ucl:student_login')
    location = get_object_or_404(Location, pk=location_id)
    token = util.prompt_for_user_token(location.spotify_username, scope='user-read-playback-state user-modify-playback-state user-read-currently-playing', client_id=location.spotipy_client_id, client_secret=location.spotipy_client_secret, redirect_uri=location.spotipy_redirect_uri)
    spotify = spotipy.Spotify(auth=token)


    song_info = spotify.currently_playing()
    if song_info == None:
        context = {
        'location' : location
        }
    else:
        image = song_info["item"]["album"]["images"][0]["url"]
        song = song_info["item"]["name"]
        artist = song_info["item"]["artists"][0]["name"]
        seconds = song_info["item"]["duration_ms"]/1000
        progress = ((song_info["progress_ms"]/1000)/seconds)*100
        context = {
            'song': song,
            'seconds': seconds,
            'progress': progress,
            'artist' :artist,
            'image' :image,
            'location' : location
        }
    return render(request, 'music/now_playing.html', context)

@staff_member_required
def setup(request, location_id):
    run_song(location_id)

    return redirect('music:location', location_id)

@background(schedule=10)
def schedule_songs(location_id):
    run_song(location_id)

def run_song(location_id):
    location = get_object_or_404(Location, pk=location_id)
    token = util.prompt_for_user_token(location.spotify_username, scope='user-read-playback-state user-modify-playback-state user-read-currently-playing', client_id=location.spotipy_client_id, client_secret=location.spotipy_client_secret, redirect_uri=location.spotipy_redirect_uri)
    spotify = spotipy.client.Spotify(auth=token)
    songs = Queue.objects.all().filter(location=location_id).order_by('-votes') 
    song = None
    if(len(songs)> 0):
        song = songs[0].song_URI
        songs[0].delete()
    
    else:
        song = spotify.user_playlist_tracks(location.spotify_username, playlist_id='spotify:playlist:1QM1qz09ZzsAPiXphF1l4S')['items'][randint(0,49)]['track']
        song = song['uri']

    device_id = spotify.devices()['devices'][0]['id']
    spotify.start_playback(device_id, uris=[song])

    song_len = spotify.track(song)['duration_ms']

    schedule_songs(location_id, schedule=int(song_len / 1000))
