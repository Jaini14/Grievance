from database import insert_grievance

def add_sample_data():
    insert_grievance(
        "Hostel washroom is very dirty and urgent",
        "Hostel", "High", "Negative", "No"
    )

    insert_grievance(
        "Library AC not working",
        "Library", "Medium", "Negative", "No"
    )

    insert_grievance(
        "Need more chairs in classroom",
        "General", "Low", "Neutral", "Yes"
    )
