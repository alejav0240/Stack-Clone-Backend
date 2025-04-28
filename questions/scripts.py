from faker import Faker
from .models import Question, Answer

fake = Faker()

def create_questions(users, tags, count=100):
    questions = []
    for _ in range(count):
        user = fake.random_element(users)
        question = Question.objects.create(
            user=user,
            title=fake.sentence(),
            body=fake.paragraph(nb_sentences=5),
        )
        question.tags.set(fake.random_elements(tags, length=fake.random_int(min=1, max=3)))
        questions.append(question)

    print(f"🎉 {len(questions)} Questions falsos creados exitosamente.")
    return questions

def create_answers(users, questions, count=300):
    answers = []
    for _ in range(count):
        user = fake.random_element(users)
        question = fake.random_element(questions)
        answer = Answer.objects.create(
            user=user,
            question=question,
            body=fake.paragraph(nb_sentences=5),
        )
        answers.append(answer)
    print(f"🎉 {len(answers)} Answers falsos creados exitosamente.")
    return answers
