from flask import Blueprint, request, jsonify
from flask_socketio import join_room, emit
from app.services.login_service.chat_service import get_chats_from_class, store_chats_in_class_wise
from datetime import datetime
from app.socketio_instance import socketio

teacher_chat_controller = Blueprint('teacher_chat_controller', __name__)

@teacher_chat_controller.route("/get_chats")
def get_chats():
    class_id = request.args.get("class_id")
    if class_id:
        try:
            messages = get_chats_from_class(class_id)
            # Ensure consistent timestamp format
            formatted_messages = []
            for msg in messages:
                # Handle possible timestamp field names
                time_stamp = msg.get('time_stamp') 
                if isinstance(time_stamp, datetime):
                    # Convert datetime to string in YYYY-MM-DD HH:mm:ss (UTC)
                    time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
                elif not time_stamp:
                    # Fallback to current UTC time if timestamp is missing
                    time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                elif not isinstance(time_stamp, str):
                    # Convert to string if timestamp is in another format
                    time_stamp = str(time_stamp)
                formatted_messages.append({
                    'sender_id': msg.get('sender_id', ''),Add the names 
                    'sender_name': msg.get('sender_name', 'Unknown'),
                    'message': msg.get('message', ''),
                    'timestamp': time_stamp,
                    'sender_role': msg.get('sender_role', 'Unknown'),
                    'class_id': msg.get('class_id', class_id)
                })
            print("Fetched messages for class", class_id, ":", formatted_messages)  # Debug log
            return jsonify(formatted_messages)
        except Exception as e:
            print(f"Error fetching chats for class {class_id}: {str(e)}")
            return jsonify({'error': 'Failed to fetch chats'}), 500
    else:
        print("No class_id provided in /get_chats")
        return jsonify([])

# --- SOCKET EVENTS ---
@socketio.on("join_class_room")
def handle_join_class(data):
    class_id = data.get("class_id")
    if class_id:
        join_room(class_id)
        print(f"Client joined class room: {class_id}")
    else:
        print("No class_id provided in join_class_room")

@socketio.on("send_message")
def handle_send_message(data):
    print("Received message data:", data)  # Debug log
    class_id = data.get('class_id')
    message = data.get('message')
    sender_id = data.get('sender_id')
    sender_role = data.get('sender_role')
    sender_name = data.get('sender_name')
    
    if not all([class_id, message, sender_id, sender_role, sender_name]):
        print("Incomplete message data:", data)
        emit("error", {"message": "Incomplete message data"})
        return

    time_stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # Store message
    store_data = {
        'sender_id': sender_id,
        'sender_role': sender_role,
        'sender_name': sender_name,
        'message': message,
        'class_id': class_id,
        'timestamp': time_stamp
    }
    try:
        store_chats_in_class_wise(store_data, time_stamp)
    except Exception as e:
        print(f"Error storing message: {str(e)}")
        emit("error", {"message": "Failed to store message"})
        return

    # Emit to all in room
    emit("receive_message", {
        "sender_id": sender_id,
        "sender_role": sender_role,
        "sender_name": sender_name,
        "message": message,
        "class_id": class_id,
        "timestamp": time_stamp
    }, room=class_id)