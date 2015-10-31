""" Media module """
import webbrowser


class Movie(object):
    """ Movie Data structure """
    def __init__(self, data):
        if data[0]:
            self.title = data[0]
        if data[1]:
            self.storyline = data[1]
        if data[2]:
            self.poster_image_url = data[2]
        if data[3]:
            self.trailer_youtube_url = data[3]
        if data[4]:
            self.release_date = data[4]
        if data[5]:
            self.director = data[5]
        if len(data) >= 7:
            self.actors = ", ".join(data[6:len(data)])

    def show_trailer(self):
        """ show trailer """
        webbrowser.open(self.trailer_youtube_url)
