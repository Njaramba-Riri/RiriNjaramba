import random

from faker import Faker

from app import db
from app.main.models import Quotes, Feedback

fake = Faker()
Faker.seed(123)
random.seed(42)

def quotes(n: int):
    
    for i in range(n):
        qts = Quotes()
        qts.email = fake.email()
        qts.name = fake.name()
        qts.service = random.choice(["Experiment Tracking", "Model development", "Web Application",
                                     "IT Consultation", "IT Support", "Model Deployment"])
        qts.description = fake.sentence()
        qts.sent = fake.date_this_decade(before_today=True, after_today=False)
        
        try:
            db.session.add(qts)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def feedback(n: int):
    for i in range(n):
        backfeed = Feedback()
        
        backfeed.name = fake.name()
        backfeed.email = random.choice([(backfeed.name).split()[0], (backfeed.name).split()[1]]) + '@gmail.com'
        backfeed.feed = fake.text(max_nb_chars=400)
        backfeed.created_at = fake.date_this_decade(before_today=True, after_today=False)
        
        try:
            db.session.add(backfeed)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
