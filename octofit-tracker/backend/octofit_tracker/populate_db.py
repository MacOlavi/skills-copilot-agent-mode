import django
import os
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

# Create test users
def create_users():
    users = []
    for i in range(5):
        user, _ = User.objects.get_or_create(username=f'user{i}', defaults={'email': f'user{i}@test.com'})
        user.set_password('testpass')
        user.save()
        users.append(user)
    return users

# Create test teams
def create_teams(users):
    teams = []
    for i in range(2):
        team, _ = Team.objects.get_or_create(name=f'Team {i}')
        team.members.set(users[i*2:i*2+3])
        team.save()
        teams.append(team)
    return teams

# Create test workouts
def create_workouts(users):
    workouts = []
    for i in range(3):
        workout, _ = Workout.objects.get_or_create(name=f'Workout {i}', defaults={'description': f'Description {i}'})
        workout.suggested_for.set(users)
        workout.save()
        workouts.append(workout)
    return workouts

# Create test activities
def create_activities(users):
    activities = []
    for user in users:
        for i in range(3):
            activity, _ = Activity.objects.get_or_create(
                user=user,
                activity_type=random.choice(['Run', 'Bike', 'Swim']),
                duration=random.randint(20, 90),
                calories_burned=random.uniform(100, 500),
                date=date.today() - timedelta(days=i)
            )
            activities.append(activity)
    return activities

# Create leaderboard entries
def create_leaderboard(users):
    for i, user in enumerate(users):
        Leaderboard.objects.get_or_create(user=user, score=random.randint(100, 1000), rank=i+1)

def main():
    users = create_users()
    create_teams(users)
    create_workouts(users)
    create_activities(users)
    create_leaderboard(users)
    print('Test data created successfully.')

if __name__ == '__main__':
    main()
