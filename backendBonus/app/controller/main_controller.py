import sqlite3
import uuid

from app.model.flight import Flight
from app.model.city import City
from app.model.plane import Aeroplane
from app.model.reservation import Reservation

import os


DB_PATH = 'db/avio.db'  # can do abs path too!
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

INIT_SCRIPT = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `rezervacija` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`let_id`	INTEGER,
	`ime`	TEXT
);
CREATE TABLE IF NOT EXISTS `let` (
	`id`	INTEGER,
	`polazni_id`	INTEGER,
	`dolazni_id`	INTEGER,
	`avion_id`	INTEGER,
	`datum`	TEXT,
	FOREIGN KEY(`dolazni_id`) REFERENCES `grad`(`id`),
	FOREIGN KEY(`polazni_id`) REFERENCES `grad`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`avion_id`) REFERENCES `avion`(`id`)
);
CREATE TABLE IF NOT EXISTS `grad` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`naziv`	TEXT
);
CREATE TABLE IF NOT EXISTS `avion` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`model`	TEXT,
	`mesta_ukupno`	INTEGER
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


def get_flights(body):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    query = """SELECT id, polazni_id, dolazni_id, avion_id, datum FROM let"""
    c.execute(query)
    ta = c.fetchall()

    use_filter = [False, False, False]

    if body is not None:
        if 'start_city' in body:
            start_city_filter = body['start_city']
            use_filter[0] = True

        if 'finish_city' in body:
            finish_city_filter = body['finish_city']
            use_filter[1] = True

        if 'date' in body:
            date_filter = body['date']
            use_filter[2] = True

    all_flights = []

    for t in ta:
        c.execute("SELECT naziv FROM grad WHERE id = ?", (t[1],))
        sc = c.fetchone()
        start_city = City(id=t[1], city_name=sc[0])

        c.execute("SELECT naziv FROM grad WHERE id = ?", (t[2],))
        fc = c.fetchone()
        finish_city = City(id=t[2], city_name=fc[0])

        c.execute("SELECT model, mesta_ukupno FROM avion WHERE id = ?", (t[3],))
        p = c.fetchone()
        plane = Aeroplane(id=t[3], model=p[0], seats=p[1])

        created_flight = Flight(id=t[0], start_city=start_city, finish_city=finish_city, plane=plane, date=t[4])

        if use_filter[0]:
            if not created_flight.start_city.city_name == start_city_filter:
                continue

        if use_filter[1]:
            if not created_flight.finish_city.city_name == finish_city_filter:
                continue

        if use_filter[2]:
            if not created_flight.date == date_filter:
                continue

        all_flights.append(created_flight)

    conn.commit()
    c.close()
    conn.close()

    return all_flights


def get_flight(flight_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()
    query = """SELECT id, polazni_id, dolazni_id, avion_id, datum FROM let WHERE id=?"""
    c.execute(query, (flight_id,))
    t = c.fetchone()

    if t is None:
        return None

    c.execute("SELECT naziv FROM grad WHERE id = ?", (t[1],))
    sc = c.fetchone()
    start_city = City(id=t[1], city_name=sc[0])

    c.execute("SELECT naziv FROM grad WHERE id = ?", (t[2],))
    fc = c.fetchone()
    finish_city = City(id=t[2], city_name=fc[0])

    c.execute("SELECT model, mesta_ukupno FROM avion WHERE id = ?", (t[3],))
    p = c.fetchone()
    plane = Aeroplane(id=t[3], model=p[0], seats=p[1])

    created_flight = Flight(id=t[0], start_city=start_city, finish_city=finish_city, plane=plane, date=t[4])

    conn.commit()
    c.close()
    conn.close()

    return created_flight


def reserve(data, flight_id):
    conn = _connect()  # todo use connection as context manager
    c = conn.cursor()

    status = -1

    plane_query = """SELECT avion_id FROM let WHERE id=?"""
    c.execute(plane_query, (flight_id,))
    p = c.fetchone()

    if p is None:
        return None

    plane_id = p[0]

    seat_query = """SELECT mesta_ukupno FROM avion WHERE id=?"""
    c.execute(seat_query, (plane_id,))
    a = c.fetchone()
    seat_max = a[0]

    c.execute("SELECT COUNT(*) FROM rezervacija WHERE let_id = ?", (flight_id,))
    s = c.fetchone()
    seat_count = s[0]

    if seat_count < seat_max:
        res_query = """INSERT INTO rezervacija (let_id, ime) VALUES (?,?)"""
        c.execute(res_query, (flight_id, data['name']))
        status = c.lastrowid

    conn.commit()
    c.close()
    conn.close()
    return status
