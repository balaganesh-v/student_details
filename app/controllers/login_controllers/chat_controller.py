from flask import Blueprint,request,jsonify
from flask_socketio import  join_room, emit
from app.services.login_service.chat_service import get_chats_from_class,store_chats_in_class_wise
from datetime import datetime
from app.socketio_instance import socketio

teacher_chat_controller = Blueprint('teacher_chat_controller', __name__)

@teacher_chat_controller.route("/get_chats")
def get_chats():
    class_id = request.args.get("class_id")
    if  class_id:
        messages = get_chats_from_class(class_id)
        return jsonify(messages)
    else:
        return jsonify([])
    
# --- SOCKET EVENTS ---
@socketio.on("join_class_room")
def handle_join_class(data):
    class_id = data.get("class_id")
    if class_id:
        join_room(class_id)
        print(f"Client joined class room: {class_id}")


@socketio.on("send_message")
def handle_send_message(data):
    print(data)
    sender_id = data.get("sender_id")
    sender_role = data.get("sender_role")
    message = data.get("message")
    class_id = data.get("class_id")
    time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    store_chats_in_class_wise(data,time_stamp)

    # Emit to all in room
    emit("receive_message", {
        'sender_id': sender_id,
        'sender_role': sender_role,
        'message': message,
        'class_id': class_id,
        'timestamp': time_stamp
    }, room=class_id)


