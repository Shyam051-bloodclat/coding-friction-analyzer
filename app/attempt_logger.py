import csv
import os


def save_attempt(
    student_name,
    problem_id,
    topic,
    difficulty,
    time_taken,
    result,
    error_type
):

    file_path = "data/attempts.csv"

    attempt_number = 1

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:

        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if (
                    row.get("student_name", "").strip() == student_name.strip()
                    and
                    row.get("problem_id", "").strip() == problem_id.strip()
                ):

                    try:
                        old_attempt = int(row.get("attempt_number", 0))

                        if old_attempt >= attempt_number:
                            attempt_number = old_attempt + 1

                    except ValueError:
                        pass


    file_exists = os.path.exists(file_path)
    file_empty = not file_exists or os.path.getsize(file_path) == 0


    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if file_empty:

            writer.writerow([
                "student_name",
                "problem_id",
                "topic",
                "difficulty",
                "attempt_number",
                "time_taken",
                "result",
                "error_type"
            ])


        writer.writerow([
            student_name,
            problem_id,
            topic,
            difficulty,
            attempt_number,
            time_taken,
            result,
            error_type
        ])