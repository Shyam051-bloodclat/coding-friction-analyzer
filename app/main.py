from flask import Flask, render_template, request
import json
import time

from code_runner import analyze_code
from attempt_logger import save_attempt


app = Flask(__name__)


with open("problems/problems.json", "r") as file:
    problems = json.load(file)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    code = ""
    student_name = ""

    if request.method == "GET":

        problem_id = list(problems.keys())[0]
        selected_problem = problems[problem_id]

        start_time = time.time()

    else:

        problem_id = request.form.get("problem")

        student_name = request.form.get("student_name", "").strip()

        code = request.form.get("code", "")

        selected_problem = problems[problem_id]

        start_time = float(
            request.form.get("start_time", time.time())
        )

        time_taken = round(time.time() - start_time, 2)

        if code.strip() and student_name:

            result = analyze_code(
                code,
                selected_problem
            )

            status = result.get("status", "")

            error_type = result.get("error_type", "")

            save_attempt(
                student_name,
                problem_id,
                selected_problem.get("topic", ""),
                selected_problem.get("difficulty", ""),
                time_taken,
                status,
                error_type
            )

        else:

            time_taken = 0

    return render_template(
        "index.html",
        problems=problems,
        result=result,
        selected_problem=selected_problem,
        code=code,
        start_time=start_time,
        student_name=student_name
    )


if __name__ == "__main__":
    app.run(debug=True)