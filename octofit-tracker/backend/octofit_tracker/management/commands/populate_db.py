
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create Users (Superheroes)
        users = [
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel),
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
            User.objects.create(name='Superman', email='superman@dc.com', team=dc),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
        ]

        # Create Workouts
        workout1 = Workout.objects.create(name='Pushups', description='Upper body workout')
        workout2 = Workout.objects.create(name='Running', description='Cardio workout')
        workout3 = Workout.objects.create(name='Squats', description='Leg workout')

        # Assign suggested workouts
        workout1.suggested_for.set(users)
        workout2.suggested_for.set(users)
        workout3.suggested_for.set(users)

        # Create Activities
        for user in users:
            Activity.objects.create(user=user, type='Pushups', duration=30, date=date.today())
            Activity.objects.create(user=user, type='Running', duration=20, date=date.today())
            Activity.objects.create(user=user, type='Squats', duration=15, date=date.today())

        # Create Leaderboard for each team
        Leaderboard.objects.create(team=marvel, points=3000)
        Leaderboard.objects.create(team=dc, points=2800)

        # Ensure unique index on email (MongoDB shell command)
        # This is best done via mongosh, but for demonstration, we show the command here:
        print('To ensure unique index on email, run in mongosh:')
        print('use octofit_db; db.users.createIndex({ "email": 1 }, { unique: true })')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
