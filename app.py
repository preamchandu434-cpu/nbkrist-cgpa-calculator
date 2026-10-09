
from flask import Flask, render_template, request
import math

app = Flask(__name__)

MAX_SEMESTERS = 12


@app.route("/", methods=["GET", "POST"])
def home():
    sgpas = ["", "", ""]
    cgpa = None
    total = None
    error = None

    if request.method == "POST":
        submitted = request.form.getlist("sgpa")

        # Check the number of semesters
        if not 1 <= len(submitted) <= MAX_SEMESTERS:
            error = "Please enter between 1 and 12 semesters."
            sgpas = submitted[:MAX_SEMESTERS] or [""]

        else:
            sgpas = submitted
            values = []

            # Validate every SGPA
            for index, item in enumerate(submitted, start=1):
                try:
                    value = float(item)
                except (ValueError, TypeError):
                    error = f"Please enter a valid SGPA for Semester {index}."
                    break

                if not math.isfinite(value) or not 0 <= value <= 10:
                    error = (
                        f"Semester {index} must have an SGPA "
                        "between 0 and 10."
                    )
                    break

                values.append(value)

            # Calculate only when every SGPA is valid
            if error is None:
                total = sum(values)
                cgpa = round(total / len(values), 2)

    return render_template(
        "index.html",
        sgpas=sgpas,
        cgpa=cgpa,
        total=total,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)