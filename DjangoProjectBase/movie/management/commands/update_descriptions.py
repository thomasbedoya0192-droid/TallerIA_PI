import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI

# Carga las variables de entorno del .env en la raíz del proyecto
load_dotenv('../.env')

class Command(BaseCommand):
    help = 'Update description of the first movie using OpenAI API'

    def handle(self, *args, **kwargs):
        # Lee la API Key de cualquiera de los dos nombres
        api_key = os.getenv('OPENAI_API_KEY') or os.getenv('openai_apikey')
        
        client = OpenAI(api_key=api_key)

        instruction = (
            "Eres un asistente de cine. Modifica la siguiente descripción de una película "
            "para que sea más atractiva, emocionante y libre de spoilers. Responde únicamente "
            "con la nueva descripción generada, sin introducciones ni textos adicionales."
        )

        movies = Movie.objects.all()
        for movie in movies:
            prompt = f"{instruction} Actualiza la descripción '{movie.description}' de la película '{movie.title}'"
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            new_desc = response.choices[0].message.content.strip()
            movie.description = new_desc
            movie.save()
            
            self.stdout.write(self.style.SUCCESS(f"Descripción actualizada para: {movie.title}"))
            break  # Mantenemos el break como pide la guía
