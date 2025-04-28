from faker import Faker
from .models import Article, Status

fake = Faker()

def create_articles(users, count=80):
    articles = []
    statuses = list(Status.objects.all())  # Obtiene todos los estados disponibles
    for _ in range(count):
        user = fake.random_element(users)
        status = fake.random_element(statuses)  # Selecciona un estado aleatorio
        article = Article.objects.create(
            user=user,
            title=fake.sentence(nb_words=6),
            body=fake.paragraph(nb_sentences=10),
            status=status,  # Asigna el estado al artículo
        )
        articles.append(article)
    print(f"🎉 {len(articles)} Articles falsos creados exitosamente.")
    return articles

def create_statuses():
    statuses = ["Publicado", "Pendiente", "Eliminado"]
    for status_name in statuses:
        Status.objects.get_or_create(name=status_name)
    print("🎉 Estados creados exitosamente.")