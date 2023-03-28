import tidalapi
from plyer import notification
session = tidalapi.Session()
login, future = session.login_oauth()

notification_title = 'Tidal OAuth Login'
notification_message = f'Open the URL to log in: {login.verification_uri_complete}'
notification.notify(title='test', message='ha')

future.result()
print(session.check_login())
album = session.album(66236918)
tracks = album.tracks()
for track in tracks:
    print(track.name)

