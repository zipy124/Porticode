from django.db import models

class Location(models.Model):
    name = models.CharField(
            max_length=100,
            help_text='Location Name')
    spotify_username = models.CharField(
            max_length=100,
            help_text='Username for Spotify')
    spotipy_client_id = models.CharField(
            max_length=100,
            help_text='Client ID for Spotipy')
    spotipy_client_secret = models.CharField(
            max_length=100,
            help_text='Client Secret for Spotipy')
    spotipy_redirect_uri = models.CharField(
            max_length=100,
            help_text='Redirect URI for Spotipy')

    def __str__(self):
        return self.name

class Queue(models.Model):
    song_URI = models.CharField(
            max_length=100,
            help_text='URI of a track')
    song_name = models.CharField(
            max_length=100,
            help_text='Song Name')
    song_artist = models.CharField(
            max_length=100,
            help_text='Song Artist')
    location = models.ForeignKey(
            Location,
            on_delete=models.CASCADE,
            null=False,
            help_text='Location of Queue')
    votes = models.IntegerField(
            default=0)
    class Meta:
        unique_together = (('location', 'song_URI'),)

    def __str__(self):
        return self.song_name + ": " + self.song_artist
