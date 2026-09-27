import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer

class Command(BaseCommand):
    help = "Generate and store TF-IDF embeddings in database for all movies"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())
        if not movies:
            self.stderr.write("No movies found in database.")
            return

        descriptions = [movie.description for movie in movies]
        
        # Generar matriz TF-IDF ajustada a 1536 dimensiones (o la cantidad de vocabularios)
        vectorizer = TfidfVectorizer(max_features=1536)
        matrix = vectorizer.fit_transform(descriptions).toarray()

        for idx, movie in enumerate(movies):
            vec = matrix[idx].astype(np.float32)
            # Asegurar padding a 1536 dimensiones
            if len(vec) < 1536:
                vec = np.pad(vec, (0, 1536 - len(vec)), 'constant')
            
            movie.emb = vec.tobytes()
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"👌 Embedding stored for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS("🌟 Finished generating embeddings for all movies."))
