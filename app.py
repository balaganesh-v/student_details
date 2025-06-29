from sample_record.load_test_record import load_all_records
from app import create_app

app = create_app()

if __name__ == "__main__":
    load_all_records()
    app.run(debug=True)
