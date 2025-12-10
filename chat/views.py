from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
import os # For our secret key, because security is no laughing matter (well, sometimes it is)!


from . import chat_bp

@chat_bp.route("/",methods=["GET","POST"])
def chat_room():
    return ""

