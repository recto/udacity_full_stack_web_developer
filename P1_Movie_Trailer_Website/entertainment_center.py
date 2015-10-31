""" script to generate movie trailer site """
import fresh_tomatoes
import media


def read_movie_data(data_file):
    """ read movie data file """
    fdata = open(data_file, "r")
    movies = []
    for line in fdata:
        data = [x.strip() for x in line.rstrip().split(",")]
        movies.append(media.Movie(data))
    fdata.close()
    return movies


def main():
    """ Main method """
    movies = read_movie_data("data.txt")
    fresh_tomatoes.open_movies_page(movies)

if __name__ == '__main__':
    main()
