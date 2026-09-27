import random
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Displays the stored embeddings of a random movie"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        if not movies:
            self.stderr.write("No movies found.")
            return

        movie = random.choice(movies)
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

        self.stdout.write(self.style.SUCCESS(f"🎬 Película seleccionada: {movie.title}"))
        self.stdout.write(f"📐 Dimensión del vector: {len(embedding_vector)}")
        self.stdout.write(f"🔢 Primeros 5 valores del embedding: {embedding_vector[:5]}")
