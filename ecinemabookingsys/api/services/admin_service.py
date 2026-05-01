from repositories.admin_repository import AdminRepository


class AdminService:
    @staticmethod
    def validate_movie_data(data):
        errors = {}

        title = data.get('title')
        genre = data.get('genre')
        status = data.get('status')
        rating = data.get('rating')

        if not title or not title.strip():
            errors['title'] = 'Movie title is required.'
        if not genre or not genre.strip():
            errors['genre'] = 'Genre is required.'
        if not status or status not in ['Currently Running', 'Coming Soon']:
            errors['status'] = 'A valid status (Currently Running or Coming Soon) is required.'
        if not rating:
            errors['rating'] = 'MPAA Rating is required.'

        return errors

    @staticmethod
    def add_movie(data):
        title = data.get('title')
        genre = data.get('genre')
        director = data.get('director')
        producer = data.get('producer')
        synopsis = data.get('synopsis')
        rating = data.get('rating')
        status = data.get('status')
        trailer_url = data.get('trailerUrl')
        poster_url = data.get('posterUrl')

        movie_id = AdminRepository.add_movie(
            title, genre, director, producer, synopsis, rating, status, trailer_url, poster_url
        )
        return movie_id

    @staticmethod
    def validate_showtime_data(data):
        errors = {}

        if not all([data.get('movie_id'), data.get('showroom_id'), data.get('show_date'), data.get('show_time')]):
            errors['fields'] = 'Missing required fields.'

        return errors

    @staticmethod
    def add_showtime(movie_id, showroom_id, show_date, show_time):
        # Check for scheduling conflict
        conflict = AdminRepository.check_showtime_conflict(showroom_id, show_date, show_time)

        if conflict:
            raise ValueError('Scheduling conflict: This showroom is already booked for this date and time.')

        AdminRepository.add_showtime(movie_id, showroom_id, show_date, show_time)
        return True

    @staticmethod
    def get_all_users():
        return AdminRepository.get_all_users()
