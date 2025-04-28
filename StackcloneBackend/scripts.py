from achievements.scripts import create_achievements, assign_user_achievements
from articles.scripts import create_articles, create_statuses
from points.scripts import create_user_points
from questions.scripts import create_questions, create_answers
from tags.scripts import create_tags
from users.scripts import create_fake_users, create_ranks
from votes.scripts import create_votes


def run_full_population():
    create_ranks()
    users = create_fake_users(50)
    tags = create_tags(20)
    create_statuses()
    questions = create_questions(users, tags, 100)
    answers = create_answers(users, questions, 300)
    create_votes(users, questions, answers, 500)
    create_articles(users, 80)
    create_user_points(users)
    achievements = create_achievements(10)
    assign_user_achievements(users, achievements)
    print("🎉 Población de datos completada exitosamente.")

