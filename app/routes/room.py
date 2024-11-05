from uuid import uuid4
import random

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.db import Session, Room


room_blueprint = Blueprint("rooms", __name__)


@room_blueprint.get("/")
def index():
    with Session() as session:
        rooms = session.query(Room).where(Room.is_reserved == False).all()
        random.shuffle(rooms)
        return render_template("index.html", rooms=rooms)


@room_blueprint.route("/add_room/", methods=["POST", "GET"])
def add_room():
    if request.method == "POST":
        with Session() as session:
            number = request.form.get("number")
            name = request.form.get("name")
            img_name_orig = None
            img_name = None
            img_url = "/static/img/default.jpg"

            photo = request.files.get("photo")
            if photo and photo.filename:
                img_name_orig = photo.filename
                img_name = uuid4().hex
                img_url = f"/static/img/{img_name}." + img_name_orig.split(".")[-1]
                photo.save("app" + img_url)

            room = Room(
                number=number,
                name=name,
                img_url=img_url,
                img_name=img_name,
                img_name_orig=img_name_orig
            )
            session.add(room)
            session.commit()
            return redirect(url_for("rooms.index"))

    return render_template("add_room.html")


@room_blueprint.get("/reserve/<int:id>")
def reserve(id):
    with Session() as session:
        room = session.query(Room).where(Room.id == id).first()
        room.is_reserved = True
        session.commit()
        return render_template("reserved.html", room=room)


@room_blueprint.get("/manage-rooms/")
def manage_rooms():
    with Session() as session:
        rooms = session.query(Room).all()
        return render_template("manage_rooms.html", rooms=rooms)


@room_blueprint.get("/delete/<int:id>")
def delete_room(id):
    with Session() as session:
        room = session.query(Room).where(Room.id == id).first()
        session.delete(room)
        session.commit()
        return redirect(url_for("rooms.manage_rooms"))


@room_blueprint.route("/edit-room/<int:id>", methods=["GET", "POST"])
def edit_room(id):
    with Session() as session:
        room = session.query(Room).where(Room.id == id).first()
        if request.method == "POST":
            room.number = request.form.get("number")
            room.name = request.form.get("name")
            room.is_reserved = True if request.form.get("is_reserved") else False

            photo = request.files.get("photo")
            if photo and photo.filename:
                room.img_name_orig = photo.filename
                room.img_name = uuid4().hex
                room.img_url = f"/static/img/{room.img_name}." + room.img_name_orig.split(".")[-1]
                photo.save("app" + room.img_url)

            session.commit()
            return redirect(url_for("rooms.manage_rooms"))

        return render_template("edit_room.html", room=room)