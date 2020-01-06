import os
import unittest
from main import app, request
from module.dbconnect import DBConnect as dbconnect


class FlaskTestCase(unittest.TestCase):
    # setup and teardown
    def setUp(self):
        self.app = app.test_client()

        self.dbpath = "test/test.db"
        with dbconnect(self.dbpath) as session:
            session.execute("CREATE TABLE post (p_uid int, pid int, title text,\
                             context text, date CURRENT_TIMESTAMP, PRIMARY KEY (pid))")
            session.execute("CREATE TABLE user (uid int, uname char(15),\
                             email char(64), PRIMARY KEY (uid))")

    def tearDown(self):
        with dbconnect(self.dbpath) as session:
            session.execute("DROP TABLE user")
            session.execute("DROP TABLE post")
        
    # test started
    def test_if_db_path_exist(self):
        self.assertTrue(os.path.exists(self.dbpath))

    def test_homepage(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_forumpage(self):
        response = self.app.get('/forum', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    