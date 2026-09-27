import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer

class Command(BaseCommand):
    help = "Calcula la similitud de coseno entre peliculas y un prompt"

    def handle(self, *args, **kwargs):
        # Seleccionamos dos películas de la base de datos
        try:
            movie1 = Movie.objects.get(title="The Matrix")
            movie2 = Movie.objects.get(title="Inception")
        except Movie.DoesNotExist:
            # Si no están con ese título exacto, tomamos las dos primeras
            movies = Movie.objects.all()[:2]
            movie1, movie2 = movies[0], movies[1]

        prompt = "película sobre ciencia ficción y realidad simulada"

        # Textos a comparar
        texts = [movie1.description, movie2.description, prompt]

        # Generar representaciones vectoriales (embeddings)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts).toarray()

        emb1 = tfidf_matrix[0]
        emb2 = tfidf_matrix[1]
        prompt_emb = tfidf_matrix[2]

        def cosine_similarity(a, b):
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return float(np.dot(a, b) / (norm_a * norm_b))

        sim_movies = cosine_similarity(emb1, emb2)
        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(self.style.SUCCESS(f"🎬 {movie1.title} vs {movie2.title}: {sim_movies:.4f}"))
        self.stdout.write(self.style.SUCCESS(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}"))
        self.stdout.write(self.style.SUCCESS(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}"))
