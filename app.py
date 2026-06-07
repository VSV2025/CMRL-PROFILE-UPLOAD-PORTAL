import os
import uuid

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory
)

from werkzeug.utils import secure_filename

from config import Config
from models import db, Submission

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Create uploads folder automatically
os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    try:

        company_name = request.form.get("company_name")
        email = request.form.get("email")
        contact_no = request.form.get("contact_number")
        pdf = request.files.get("company_profile")

        if not company_name:
            return "Company Name is required", 400

        if not email:
            return "Email is required", 400

        if not contact_no:
            return "Contact Number is required", 400

        if not pdf:
            return "PDF file is required", 400

        if pdf.filename == "":
            return "Please select a PDF file", 400

        if not allowed_file(pdf.filename):
            return "Only PDF files are allowed", 400

        filename = (
            str(uuid.uuid4())
            + "_"
            + secure_filename(pdf.filename)
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        pdf.save(filepath)

        submission = Submission(
            company_name=company_name,
            email=email,
            contact_no=contact_no,
            pdf_path=filename
        )

        db.session.add(submission)
        db.session.commit()

        return """
        <html>
        <body style="font-family:Arial;text-align:center;padding-top:80px;">
            <h2 style="color:green;">
                Submission Successful!
            </h2>

            <p>
                Your company profile has been uploaded successfully.
            </p>

            <br>

            <a href="/">
                Submit Another Profile
            </a>
        </body>
        </html>
        """

    except Exception as e:

        return f"""
        <html>
        <body style="font-family:Arial;padding:30px;">
            <h2 style="color:red;">
                Error Occurred
            </h2>

            <pre>{str(e)}</pre>
        </body>
        </html>
        """, 500


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.route("/admin/submissions")
def submissions():

    data = Submission.query.order_by(
        Submission.created_at.desc()
    ).all()

    result = []

    for item in data:

        result.append({
            "id": item.id,
            "company_name": item.company_name,
            "email": item.email,
            "contact_no": item.contact_no,
            "pdf_link": f"/uploads/{item.pdf_path}",
            "created_at": str(item.created_at)
        })

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
