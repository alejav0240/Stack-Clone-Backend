from faker import Faker
from .models import Tag

fake = Faker()

def create_tags(count=20):
    tags = []
    for _ in range(count):
        tag_name = fake.word().lower()
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)

    print(f"🎉 {len(tags)} Tags falsos creados exitosamente.")
    return tags
