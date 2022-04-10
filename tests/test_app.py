from flask import url_for, request, redirect,render_template
from flask_testing import TestCase
from app import app, db, Todo
from datetime import datetime

class TestBase(TestCase):

    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
        SECRET_KEY='TEST_SECRET_KEY',
        DEBUG=True,
        WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()
        test_task = Todo(content="Mop floors")
        db.session.add(test_task)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestAdd(TestBase):
    def test_home_get(self):
        response= self.client.get(url_for('hello_internet'))
        self.assert200
    
    def test_post_task(self):
        response = self.client.post(url_for("hello_internet"), data = dict(content="Call mum"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        test = Todo.query.filter_by(content="Call mum").first()
        assert test.id == 2

    def test_post_task2(self):
        response = self.client.post(url_for("hello_internet"), data = dict(content="Call mum again"), follow_redirects=True)
        self.assertIn(b'again', response.data)


class TestDelete(TestBase):
    def test_delete_task(self):
        response = self.client.get(url_for('delete', id=1), follow_redirects=True)
        assert len(Todo.query.all()) == 0
