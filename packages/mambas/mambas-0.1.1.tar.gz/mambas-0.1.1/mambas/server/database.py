import datetime
import json
import pkg_resources
import sqlite3

from mambas.server import models

class MambasDatabase():

    def __init__(self):
        self.db_path = pkg_resources.resource_filename(__package__, "resources/database.db")
        self.init()

    # PROJECTS --------------------------------------------------------------------------

    def create_project(self, name, token):
        query = "INSERT INTO projects (name, token) VALUES (?, ?)"
        vars = (name, token)
        id_project = self.query(query, vars).lastrowid
        project = self.get_project(id_project)
        return project

    def get_project(self, id_project):
        query = "SELECT id_project, name, session_counter, token FROM projects WHERE id_project = ?"
        vars = [id_project]
        rows = self.query(query, vars).fetchall()
        project = None
        if len(rows) > 0:
            row = rows[0]
            id_project = row[0]
            name = row[1]
            session_counter = row[2]
            token = row[3]
            project = models.Project(id_project, name, session_counter, token)
        return project

    def get_project_by_token(self, token):
        query = "SELECT id_project, name, session_counter, token FROM projects WHERE token = ?"
        vars = [token]
        rows = self.query(query, vars).fetchall()
        project = None
        if len(rows) > 0:
            row = rows[0]
            id_project = row[0]
            name = row[1]
            session_counter = row[2]
            token = row[3]
            project = models.Project(id_project, name, session_counter, token)
        return project

    def get_all_projects(self):
        query = "SELECT id_project, name, session_counter, token FROM projects"
        rows = self.query(query).fetchall()
        projects = []
        for row in rows:
            id_project = row[0]
            name = row[1]
            session_counter = row[2]
            token = row[3]
            projects.append(models.Project(id_project, name, session_counter, token))
        return projects

    def increment_project_session_counter(self, id_project):
        query = "UPDATE projects SET session_counter = session_counter + 1 WHERE id_project = ?"
        vars = [id_project]
        self.query(query, vars)
        project = self.get_project(id_project)
        return project

    def delete_project(self, id_project):
        query = "DELETE FROM projects WHERE id_project = ?"
        vars = [id_project]
        result = self.query(query, vars).rowcount
        return result > 0

    # SESSIONS --------------------------------------------------------------------------

    def create_session_for_project(self, session_index, host, id_project):
        query = "INSERT INTO sessions (session_index, host, id_project) VALUES (?, ?, ?)"
        vars = (session_index, host, id_project)
        id_session = self.query(query, vars).lastrowid
        session = self.get_session(id_session)
        return session

    def get_session(self, id_session):
        query = "SELECT id_session, session_index, dt_start, dt_end, is_active, host, id_project FROM sessions WHERE id_session = ?"
        vars = [id_session]
        rows = self.query(query, vars).fetchall()
        session = None
        if len(rows) > 0:
            row = rows[0]
            id_session = row[0]
            session_index = row[1]
            dt_start = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S") if row[2] is not None else None
            dt_end = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") if row[3] is not None else None
            is_active = row[4]
            host = row[5]
            id_project = row[6]
            session = models.Session(id_session, session_index, dt_start, dt_end, is_active, host, id_project)
        return session

    def get_sessions_for_project(self, id_project):
        query = "SELECT id_session, session_index, dt_start, dt_end, is_active, host, id_project FROM sessions WHERE id_project = ?"
        vars = [id_project]
        rows = self.query(query, vars).fetchall()
        sessions = []
        for row in rows:
            id_session = row[0]
            session_index = row[1]
            dt_start = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S") if row[2] is not None else None
            dt_end = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") if row[3] is not None else None
            is_active = row[4]
            host = row[5]
            id_project = row[6]
            sessions.append(models.Session(id_session, session_index, dt_start, dt_end, is_active, host, id_project))
        return sessions

    def set_session_inactive(self, id_session):
        query = "UPDATE sessions SET is_active = 0 WHERE id_session = ?"
        vars = [id_session]
        self.query(query, vars)
        session = self.get_session(id_session)
        return session

    def set_session_start_time(self, id_session, dt_start):
        query = "UPDATE sessions SET dt_start = ? WHERE id_session = ?"
        vars = (dt_start.strftime("%Y-%m-%d %H:%M:%S"), id_session)
        self.query(query, vars)
        session = self.get_session(id_session)
        return session

    def set_session_end_time(self, id_session, dt_end):
        query = "UPDATE sessions SET dt_end = ? WHERE id_session = ?"
        vars = (dt_end.strftime("%Y-%m-%d %H:%M:%S"), id_session)
        self.query(query, vars)
        session = self.get_session(id_session)
        return session

    def delete_session(self, id_session):
        query = "DELETE FROM sessions WHERE id_session = ?"
        vars = [id_session]
        result = self.query(query, vars).rowcount
        return result > 0

    # EPOCHS ----------------------------------------------------------------------------

    def create_epoch_for_session(self, index, metrics, time, id_session):
        query = "INSERT INTO epochs (epoch_index, metrics, time, id_session) VALUES (?, ?, ?, ?)"
        vars = (index, json.dumps(metrics), time.strftime("%Y-%m-%d %H:%M:%S"), id_session)
        id_epoch = self.query(query, vars).lastrowid
        epoch = self.get_epoch(id_epoch)
        return epoch

    def get_epoch(self, id_epoch):
        query = "SELECT id_epoch, epoch_index, metrics, time, id_session FROM epochs WHERE id_epoch = ?"
        vars = [id_epoch]
        rows = self.query(query, vars).fetchall()
        epoch = None
        if len(rows) > 0:
            row = rows[0]
            id_epoch = row[0]
            index = row[1]
            metrics = json.loads(row[2].replace("'", '"'))
            time = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
            id_session = row[4]
            epoch = models.Epoch(id_epoch, index, metrics, time, id_session)
        return epoch

    def get_epochs_for_session(self, id_session):
        query = "SELECT id_epoch, epoch_index, metrics, time, id_session FROM epochs WHERE id_session = ?"
        vars = [id_session]
        rows = self.query(query, vars).fetchall()
        epochs = []
        for row in rows:
            id_epoch = row[0]
            index = row[1]
            metrics = json.loads(row[2].replace("'", '"'))
            time = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
            id_session = row[4]
            epochs.append(models.Epoch(id_epoch, index, metrics, time, id_session))
        return epochs

    def delete_epoch(self, id_epoch):
        query = "DELETE FROM epochs WHERE id_epoch = ?"
        vars = [id_epoch]
        result = self.query(query, vars).rowcount
        return result > 0

    # UTILS ----------------------------------------------------------------------------

    def init(self):
        conn = sqlite3.connect(self.db_path)
        with conn:
            cursor = conn.cursor()
            db_init_path = pkg_resources.resource_filename(__package__, "resources/init_db.sql")
            sql = open(db_init_path, "r").read()
            cursor.executescript(sql)

    def query(self, query, vars=[]):
        conn = sqlite3.connect(self.db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, vars)
            return cursor