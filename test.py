from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u = User(username='Moss')
		u.set_password('moose')
		self.assertFalse(u.check_password('mousse'))
		self.assertTrue(u.check_password('moose'))

	def test_avatar(self):
		u = User(username='mohsin', email='moss@moose.com')
		self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'a23e0bae22b8b4964f8cedd8f0e010da'
                                         '?d=identicon&s=128'))

	def test_follow(self):
		u1 = User(username='Moss', email='mohsin@moose.com')
		u2 = User(username='mohsin', email='moss@moose.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(), [])
		self.assertEqual(u1.followers.all(), [])

		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 1)
		self.assertEqual(u1.followed.first().username, 'mohsin')
		self.assertEqual(u2.followers.count(), 1)
		self.assertEqual(u2.followers.first().username, 'Moss')

		u1.unfollow(u2)
		db.session.commit()
		self.assertFalse(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 0)
		self.assertEqual(u2.followers.count(), 0)

	def test_follow_posts(self):
		#create four users
		u1 = User(username='Moss', email='mohsin@moose.com')
		u2 = User(username='mohsin', email='moss@moose.com')
		u3 = User(username='ocelot', email='revolver@moose.com')
		u4 = User(username='snake', email='john@moose.com')
		db.session.add_all([u1, u2, u3, u4])

		#create four posts
		now = datetime.utcnow()
		p1 = Post(body="ima moss", author=u1,
				timestamp=now + timedelta(seconds=1))
		p2 = Post(body="I'm Mohsin", author=u2, 
				timestamp=now + timedelta(seconds=4))
		p3 = Post(body="Meow", author=u3, 
				timestamp=now + timedelta(seconds=3))
		p4 = Post(body="Metal Gear", author=u4, 
				timestamp=now + timedelta(seconds=2))
		db.session.add_all([p1, p2, p3, p4])
		db.session.commit()

		#setup the followers
		u1.follow(u2) #Moss follows mohsin
		u1.follow(u4) #Moss follows snake
		u2.follow(u3) #mohsin follows ocelot
		u3.follow(u4) #ocelot follows snake
		db.session.commit()

		#check the followed posts of each user
		f1 = u1.followed_posts().all()
		f2 = u2.followed_posts().all()
		f3 = u3.followed_posts().all()
		f4 = u4.followed_posts().all()
		self.assertEqual(f1, [p2, p4, p1])
		self.assertEqual(f2, [p2, p3])
		self.assertEqual(f3, [p3, p4])
		self.assertEqual(f4, [p4])

if __name__ == '__main__':
	unittest.main(verbosity=2)
