import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib.parse
from django.shortcuts import render
from .models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year).count()
            movie_counts_by_year[year] = movies_in_year
        else:
            movie_counts_by_year['Unknown'] = Movie.objects.filter(year__isnull=True).count()

    bar_width = 0.5
    movie_positions = range(len(movie_counts_by_year))

    plt.bar(movie_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.xticks(movie_positions, movie_counts_by_year.keys(), rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.title('Movies per year')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = urllib.parse.quote(base64.b64encode(image_png)) if 'base64' in locals() else urllib.parse.quote(image_png)

    return render(request, 'statistics.html', {'graphic': graphic})

def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def recommend(request):
    search_prompt = request.GET.get('prompt', '')
    recommended_movie = None
    similarity_score = 0

    if search_prompt:
        movies = list(Movie.objects.all())
        if movies:
            descriptions = [m.description for m in movies] + [search_prompt]
            
            vectorizer = TfidfVectorizer(max_features=1536)
            matrix = vectorizer.fit_transform(descriptions).toarray()

            prompt_vec = matrix[-1].astype(np.float32)
            if len(prompt_vec) < 1536:
                prompt_vec = np.pad(prompt_vec, (0, 1536 - len(prompt_vec)), 'constant')

            max_sim = -1
            best_movie = None

            for idx, movie in enumerate(movies):
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                sim = cosine_similarity(prompt_vec, movie_emb)
                if sim > max_sim:
                    max_sim = sim
                    best_movie = movie

            recommended_movie = best_movie
            similarity_score = max_sim

    return render(request, 'recommend.html', {
        'prompt': search_prompt,
        'movie': recommended_movie,
        'similarity': round(similarity_score, 4)
    })
