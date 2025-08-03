from config.db_config import db_connection

# Fetch chat messages for a specific class
def get_chats_from_class_by_db(class_id):
    connection = None
    cursor = None
    try:
        connection = db_connection()
        cursor = connection.cursor()  # Ensures results are returned as dicts

        cursor.execute("""
            SELECT sender_id, sender_role, message, time_stamp
            FROM chat_messages
            WHERE class_name = %s
            ORDER BY time_stamp ASC
        """, (class_id,))

        messages = cursor.fetchall()

        if not messages:
            return [{
                "sender_id": "System",
                "sender_role": "system",
                "message": "Newly started the group",
                "time_stamp": None
            }]

        return messages

    except Exception as e:
        print(f"[DB ERROR] Failed to fetch chats for class '{class_id}': {e}")
        return [{
            "sender_id": "System",
            "sender_role": "system",
            "message": "Error loading messages.",
            "time_stamp": None
        }]
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Store a new chat message into the database
def store_chats_in_class_wise_into_db(data, time_stamp):
    connection = None
    cursor = None
    try:
        connection = db_connection()
        cursor = connection.cursor()

        sender_id = data.get("sender_id")
        sender_role = data.get("sender_role")
        message = data.get("message")
        class_name = data.get("class_id")

        query = """
            INSERT INTO chat_messages (sender_id, sender_role, message, class_name, time_stamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (sender_id, sender_role, message, class_name, time_stamp)
        cursor.execute(query, values)
        connection.commit()

        return True

    except Exception as e:
        print(f"[DB ERROR] Failed to store chat: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
