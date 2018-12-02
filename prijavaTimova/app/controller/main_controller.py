import sqlite3
import uuid

from ..model.team import Team
from ..model.team_member import TeamMember

import os

DB_PATH = 'db/hzs.db'  # can do abs path too!
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

INIT_SCRIPT = """
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "team_member" (
  `id`           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `first_name`   TEXT    NOT NULL,
  `last_name`    TEXT    NOT NULL,
  `email`        TEXT    NOT NULL,
  `phone_number` TEXT,
  `school`       TEXT,
  `city`         TEXT,
  `team_id`      INTEGER NOT NULL,
  FOREIGN KEY (`team_id`) REFERENCES team (`id`)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `team` (
  `id`          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name`        TEXT    NOT NULL,
  `description` TEXT,
  `photo_url`   TEXT,
  `team_uuid`   TEXT
);
COMMIT;
"""


def _connect():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    return conn


conn = _connect()
c = conn.cursor()
c.executescript(INIT_SCRIPT)
conn.commit()
conn.close()


def get_all_teams():
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    query = """SELECT id, name, description, photo_url, team_uuid FROM team"""
    c.execute(query)
    result_set = c.fetchall()

    teams = []

    for t in result_set:
        created_team = Team(id=t[0], name=t[1], description=t[2], photo_url=t[3], team_uuid=t[4])

        member_query = """SELECT id, first_name, last_name, email, phone_number, school, city FROM 
        team_member WHERE team_id=?"""
        c.execute(member_query, (created_team.id,))
        members = c.fetchall()

        for m in members:
            created_member = TeamMember(id=m[0], first_name=m[1], last_name=m[2], email=m[3], phone_number=m[4],
                                        school=m[5], city=m[6], team=created_team)
            created_team.add_member(created_member)

        teams.append(created_team)

    conn.commit()
    c.close()
    conn.close()

    return teams


def get_team(team_uuid):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    query = """SELECT id, name, description, photo_url, team_uuid FROM team WHERE team_uuid=?"""
    c.execute(query, (team_uuid,))
    t = c.fetchone()

    if t is None:
        return None

    created_team = Team(id=t[0], name=t[1], description=t[2], photo_url=t[3], team_uuid=t[4])

    member_query = """SELECT id, first_name, last_name, email, phone_number, school, city FROM 
    team_member WHERE team_id=?"""
    c.execute(member_query, (created_team.id,))
    members = c.fetchall()

    for m in members:
        created_member = TeamMember(id=m[0], first_name=m[1], last_name=m[2], email=m[3], phone_number=m[4],
                                    school=m[5], city=m[6], team=created_team)
        created_team.add_member(created_member)

    conn.commit()
    c.close()
    conn.close()

    return created_team


def create_team(data):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    error_check = check_team(data)
    if error_check != 4:
        return error_check

    team_query = """INSERT INTO team (name, description, photo_url, team_uuid) VALUES (?,?,?,?)"""
    team_uuid = uuid.uuid4()
    c.execute(team_query, (data['name'], data['description'], data['photo_url'], str(team_uuid)))
    team_id = c.lastrowid
    data['id'] = team_id
    data['team_uuid'] = team_uuid

    for m in data['team_members']:
        member_query = """INSERT INTO team_member (first_name, last_name, email, phone_number, school, city, team_id) 
        VALUES (?,?,?,?,?,?,?)"""
        c.execute(member_query,
                  (m['first_name'], m['last_name'], m['email'], m['phone_number'], m['school'], m['city'], team_id))
        m['id'] = c.lastrowid

    conn.commit()
    c.close()
    conn.close()
    return data


def update_team(data, team_uuid):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    query = """SELECT id FROM team WHERE team_uuid=?"""
    c.execute(query, (team_uuid,))
    t = c.fetchone()

    if t is None:
        return None

    team_id = t[0]

    error_check = check_team(data)
    if error_check != 4:
        return error_check

    delete_all_team_members(team_id)

    team_query = """UPDATE team SET name=?, description=?, photo_url=? WHERE team_uuid=?"""

    c.execute(team_query, (data['name'], data['description'], data['photo_url'], team_uuid))

    for m in data['team_members']:
        member_query = """INSERT INTO team_member (first_name, last_name, email, phone_number, school, city, team_id) 
        VALUES (?,?,?,?,?,?,?)"""
        c.execute(member_query,
                  (m['first_name'], m['last_name'], m['email'], m['phone_number'], m['school'], m['city'], team_id))
        m['id'] = c.lastrowid

    conn.commit()
    c.close()
    conn.close()
    return data


def delete_team(team_uuid):
    conn = _connect()

    with conn:
        team_query = """DELETE FROM team WHERE team_uuid=?"""
        status = conn.execute(team_query, (team_uuid,))
        success = False
        if status.rowcount == 1:
            success = True

    return success


def delete_all_team_members(team_id):
    conn = _connect()
    try:
        with conn:
            team_query = """DELETE FROM team_member WHERE team_id=?"""
            status = conn.execute(team_query, (team_id,))
            success = False
            if status.rowcount > 0:
                success = True

            return success
    except sqlite3.Error:
        return False


def check_team(data):
    if 'name' not in data or 'description' not in data or 'photo_url' not in data:
        return -1  # error no field

    if data["name"] == '' or data["description"] == '' or data["photo_url"] == '':
        return -1  # error field empty

    member_count = 0
    for m in data['team_members']:
        member_count += 1
        member_faulty = check_team_member(m)
        if member_faulty:
            return 2, member_count  # member error

    if member_count < 3 or member_count > 4:
        return 3, member_count  # error wrong member count
    return 4  # no error


def check_team_member(m):
    if 'first_name' not in m or 'last_name' not in m or 'email' not in m or \
            'phone_number' not in m or 'school' not in m or 'city' not in m:
        return True  # error no member field

    if m['first_name'] == '' or m['last_name'] == '' or m['email'] == '' or \
            m['phone_number'] == '' or m['school'] == '' or m['city'] == '':
        return True  # error member field empty
    return False


def get_team_member(team_member_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    member_query = """SELECT id, first_name, last_name, email, phone_number, school, city, team_id FROM 
    team_member WHERE id=?"""
    c.execute(member_query, (team_member_id,))
    m = c.fetchone()

    if m is None:
        return None

    dummy_team = Team(id=m[7], name="dummy", description="dummy", photo_url="dummy", team_uuid="dummy")
    created_member = TeamMember(id=m[0], first_name=m[1], last_name=m[2], email=m[3], phone_number=m[4],
                                school=m[5], city=m[6], team=dummy_team)

    conn.commit()
    c.close()
    conn.close()

    return created_member


def update_team_member(m, team_member_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    member_faulty = check_team_member(m)
    if member_faulty:
        return 2  # member error

    member_update = """UPDATE team_member SET first_name = ?, last_name = ?, email = ?,
        phone_number = ?, school = ?, city= ? WHERE id = ?"""
    c.execute(member_update, (m['first_name'], m['last_name'], m['email'],
                              m['phone_number'], m['school'], m['city'], team_member_id))
    if c.rowcount < 1:
        return None

    conn.commit()
    c.close()
    conn.close()
    return m


def delete_team_member(team_member_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    member_query = """SELECT team_id FROM team_member WHERE id=?"""
    c.execute(member_query, (team_member_id,))
    team = c.fetchone()

    if team is None:
        return None

    team_id = team[0]

    count_members = """SELECT count(*) FROM team_member WHERE team_id = ?;"""
    c.execute(count_members, (team_id,))
    team_length = c.fetchone()

    if team_length[0] < 4:
        return 2  # too little members

    with conn:
        team_query = """DELETE FROM team_member WHERE id=?"""
        status = conn.execute(team_query, (team_member_id,))
        success = False
        if status.rowcount == 1:
            success = True

    return success
