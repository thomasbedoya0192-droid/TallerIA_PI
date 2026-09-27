import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie image paths in the database using default or available images"

    def handle(self, *args, **kwargs):
        images_folder = os.path.join('media', 'movie', 'images')
        default_image = os.path.join('movie', 'images', 'default.JPG')

        movies = Movie.objects.all()
        updated_count = 0

        for movie in movies:
            image_filename = f"m_{movie.title}.png"
            image_path_full = os.path.join(images_folder, image_filename)

            # Si existe la imagen individual la asigna, de lo contrario asigna default.JPG
            if os.path.exists(image_path_full):
                movie.image = os.path.join('movie', 'images', image_filename)
            else:
                movie.image = default_image

            movie.save()
            updated_count += 1
            self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movie images."))
