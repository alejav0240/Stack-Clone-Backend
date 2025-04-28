from faker import Faker
from .models import Vote

fake = Faker()

def create_votes(users, questions, answers, count=500):
    for _ in range(count):
        user = fake.random_element(users)
        vote_type = fake.random_element(elements=('upvote', 'downvote'))

        if fake.boolean(chance_of_getting_true=50):
            target = fake.random_element(questions)
            Vote.objects.create(
                user=user,
                question=target,
                vote_type=vote_type,
            )
        else:
            target = fake.random_element(answers)
            Vote.objects.create(
                user=user,
                answer=target,
                vote_type=vote_type,
            )
    print(f"🎉 Votes falsos creados exitosamente.")
