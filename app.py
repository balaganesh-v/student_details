# ✅ Monkey patch FIRST
import eventlet
eventlet.monkey_patch()

from app import create_app, socketio
from app.sample_record.load_test_record import load_all_records

app = create_app()

if __name__ == "__main__":
    try:
        load_all_records()
        print("✅ Test records loaded successfully.")
    except Exception as e:
        print(f"⚠️ Failed to load test records: {e}")
    
    print("🚀 Starting SocketIO server...")

    # Print the accessible link at the bottom
    print("\n🌐 App running at: http://localhost:5000/\n")

    socketio.run(app, host="127.0.0.1", port=5000)
