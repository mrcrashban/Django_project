import random

from django.core.management.base import BaseCommand
from mimesis import Person
from mimesis.locales import Locale
from askinside.models import Question, Tag, Vote, Answer, Profile
from django.contrib.auth.models import User
from mimesis import Text


class Command(BaseCommand):
    help = 'Fill database with randomized content'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Indicates the number of rows to be created')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        _fill_users(ratio)
        _fill_tags(ratio)
        _fill_questions(10*ratio)
        _fill_answers(100*ratio)
        _fill_votes(500*ratio)


def _fill_users(ratio):
    print('Creating users...')
    users = []
    for _ in range(ratio):
        person = Person(Locale.EN)

        u = User(first_name=person.first_name(),
                 last_name=person.last_name(),
                 email=person.email(),
                 password=person.password(),
                 is_staff=False,
                 username=person.username(),
                 )

        users.append(u)

    User.objects.bulk_create(users, ignore_conflicts=True)

    persisted_users = User.objects.all()
    profiles = []
    for user in persisted_users:
        profiles.append(Profile(user=user))
    Profile.objects.bulk_create(profiles, ignore_conflicts=True)


def _fill_tags(ratio):
    print('Creating tags...')
    tags = []
    for _ in range(ratio):
        txt = Text(Locale.EN)

        t = Tag(title=txt.word())
        tags.append(t)
    Tag.objects.bulk_create(tags, ignore_conflicts=True)


def _fill_questions(ratio):
    print('Creating questions...')

    users = list(User.objects.all())
    random.shuffle(users)

    questions = []
    for i in range(ratio):
        txt = Text(Locale.EN)

        q = Question(title=txt.quote(),
                     body=txt.text(30),
                     author=users[i % (len(users) or 1)],
                     )

        questions.append(q)

    Question.objects.bulk_create(questions, ignore_conflicts=True)

    persisted_questions = Question.objects.all()

    all_tags = Tag.objects.all()
    for i in range(ratio):
        persisted_questions[i].tags.set(random.sample(list(all_tags), random.randint(0, 5)))
        persisted_questions[i].save()


def _fill_answers(ratio):
    print('Creating answers...')

    users = list(User.objects.all())
    random.shuffle(users)
    questions = list(Question.objects.all())
    random.shuffle(questions)

    n = 10
    for j in range(n):
        print(f'Creating answers #{j + 1}...')
        answers = []
        for i in range(ratio // n):
            txt = Text(Locale.EN)
            a = Answer(body=txt.text(30), author=users[i % (len(users) or 1)],
                       question=questions[i % (len(questions) or 1)], is_correct=False)
            answers.append(a)
        Answer.objects.bulk_create(answers, ignore_conflicts=True)


def _fill_votes(ratio):
    print('Creating votes...')

    random_model_instances = list(Question.objects.all()) + list(Answer.objects.all())
    random.shuffle(random_model_instances)
    print(f"random model len: {len(random_model_instances)}")
    users = list(User.objects.all())
    print(f"user len: {len(users)}")

    n = 500
    for j in range(n):
        print(f'Creating votes #{j + 1}...')
        votes = []
        for i in range(ratio // n):
            rates = [-1, 1]
            v = Vote(
                rate=random.sample(rates, 1)[0],
                author=random.sample(users, 1)[0],
                content_object=random.sample(random_model_instances, 1)[0]
            )
            votes.append(v)
        print(f"votes length {len(votes)}")
        Vote.objects.bulk_create(votes, ignore_conflicts=True)
