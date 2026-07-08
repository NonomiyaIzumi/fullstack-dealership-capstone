"""Assemble submission.pdf from the project's real files and submission_assets/."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "submission_assets"

REPO_URL = "https://github.com/NonomiyaIzumi/fullstack-dealership-capstone"
BLOB = f"{REPO_URL}/blob/master"

ASCII_REPLACEMENTS = {
    "—": "-", "–": "-",
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "…": "...",
    "✓": "[OK]",
    "·": "-",
    "│": "|",
}


def to_latin1(text):
    for unicode_char, ascii_char in ASCII_REPLACEMENTS.items():
        text = text.replace(unicode_char, ascii_char)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def read_code(relative_path):
    return to_latin1((ROOT / relative_path).read_text(encoding="utf-8"))


def read_asset_text(filename):
    return to_latin1((ASSETS / filename).read_text(encoding="utf-8"))


class SubmissionPDF(FPDF):
    """PDF builder for the Full Stack Application Development Capstone submission."""

    def task_header(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 10, to_latin1(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_header(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 8, to_latin1(title), new_x="LMARGIN", new_y="NEXT")

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, to_latin1(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def note_text(self, text):
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(150, 90, 0)
        self.multi_cell(0, 5, to_latin1(text), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def code_block(self, code):
        self.set_font("Courier", "", 8)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 4, to_latin1(code), fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def screenshot(self, filename, w=180):
        path = ASSETS / filename
        self.image(str(path), w=w)
        self.ln(2)


def build():
    pdf = SubmissionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)

    # --- Title page --------------------------------------------------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.multi_cell(0, 12, "Full Stack Application Development Capstone Project", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, "Cars Dealership - IBM Skills Network Capstone Submission", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, f"Repository: {REPO_URL}", new_x="LMARGIN", new_y="NEXT")

    # --- Task 1 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 1: README.md with project name (1 point)")
    pdf.sub_header(f"GitHub URL: {BLOB}/README.md")

    # --- Task 2 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 2: django_server terminal output (1 point)")
    pdf.code_block(read_asset_text("django_server"))

    # --- Task 3 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 3: server/frontend/static/About.html (3 points)")
    pdf.sub_header(f"GitHub URL: {BLOB}/server/frontend/static/About.html")
    pdf.code_block(read_code("server/frontend/static/About.html"))

    # --- Task 4 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 4: server/frontend/static/Contact.html (2 points)")
    pdf.sub_header(f"GitHub URL: {BLOB}/server/frontend/static/Contact.html")
    pdf.code_block(read_code("server/frontend/static/Contact.html"))

    # --- Task 5 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 5: loginuser cURL command + output (2 points)")
    pdf.code_block(read_asset_text("loginuser"))

    # --- Task 6 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 6: logoutuser cURL command + output (2 points)")
    pdf.code_block(read_asset_text("logoutuser"))

    # --- Task 7 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 7: server/frontend/src/components/Register/Register.jsx (1 point)")
    pdf.sub_header(f"GitHub URL: {BLOB}/server/frontend/src/components/Register/Register.jsx")
    pdf.code_block(read_code("server/frontend/src/components/Register/Register.jsx"))

    # --- Task 8 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 8: getdealerreviews cURL command + output (2 points)")
    pdf.code_block(read_asset_text("getdealerreviews"))

    # --- Task 9 --------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 9: getalldealers cURL command + output (2 points)")
    pdf.code_block(read_asset_text("getalldealers"))

    # --- Task 10 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 10: getdealerbyid cURL command + output (2 points)")
    pdf.code_block(read_asset_text("getdealerbyid"))

    # --- Task 11 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 11: getdealersbyState (Kansas) cURL command + output (2 points)")
    pdf.code_block(read_asset_text("getdealersbyState"))

    # --- Task 12 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 12: admin_login screenshot (2 points)")
    pdf.body_text("Root user (admin) logged in on the Django admin site.")
    pdf.screenshot("admin_login.png")

    # --- Task 13 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 13: admin_logout screenshot (1 point)")
    pdf.body_text("Root user logged out of the Django admin site.")
    pdf.screenshot("admin_logout.png")

    # --- Task 14 & 15 ----------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 14 & 15: getallcarmakes cURL command + output (4 points)")
    pdf.code_block(read_asset_text("getallcarmakes"))

    # --- Task 16 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header('Task 16: analyzereview - sentiment for "Fantastic services" (2 points)')
    pdf.code_block(read_asset_text("analyzereview"))

    # --- Task 17 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 17: get_dealers screenshot - home page before login (1 point)")
    pdf.screenshot("get_dealers.png")

    # --- Task 18 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 18: get_dealers_loggedin screenshot - home page after login (2 points)")
    pdf.body_text("Shows the Review Dealer option, the logged-in username (janedoe), and the URL in the address bar.")
    pdf.screenshot("get_dealers_loggedin.png")

    # --- Task 19 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 19: dealersbystate screenshot - filtered by Kansas (2 points)")
    pdf.screenshot("dealersbystate.png")

    # --- Task 20 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 20: dealer_id_reviews screenshot - dealer detail + reviews (1 point)")
    pdf.screenshot("dealer_id_reviews.png")

    # --- Task 21 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 21: dealership_review_submission screenshot - review form before submit (1 point)")
    pdf.screenshot("dealership_review_submission.png")

    # --- Task 22 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 22: added_review screenshot - posted review visible (2 points)")
    pdf.screenshot("added_review.png")

    # --- Task 23 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 23: CICD - GitHub Actions workflow run output (3 points)")
    pdf.sub_header(f"Workflow: {REPO_URL}/actions")
    pdf.code_block(read_asset_text("CICD"))

    # --- Task 24 -------------------------------------------------------------------
    pdf.add_page()
    pdf.task_header("Task 24: deploymentURL (1 point)")
    deployment_url_file = ASSETS / "deploymentURL"
    if deployment_url_file.exists():
        pdf.code_block(read_asset_text("deploymentURL"))
    else:
        pdf.note_text(
            "Pending: no cloud account/CLI (IBM Cloud, Docker) was available in the build "
            "environment, so this project is configured for a one-time manual deploy to "
            "Render's free tier instead (see DEPLOYMENT.md in the repo root - a render.yaml "
            "Blueprint deploys all three services). Once deployed, the live URL goes here."
        )

    # --- Task 25-28 (deployed screenshots) ------------------------------------------
    deployed_tasks = [
        ("Task 25", "deployed_landingpage", "Deployed landing page (2 points)"),
        ("Task 26", "deployed_loggedin", "Deployed logged-in page, showing the username (2 points)"),
        ("Task 27", "deployed_dealer_detail", "Deployed dealer detail page (2 points)"),
        ("Task 28", "deployed_add_review", "Deployed page showing a posted review (2 points)"),
    ]
    for task_label, base_name, title in deployed_tasks:
        pdf.add_page()
        pdf.task_header(f"{task_label}: {title}")
        found = None
        for ext in (".png", ".jpeg", ".jpg"):
            candidate = ASSETS / f"{base_name}{ext}"
            if candidate.exists():
                found = candidate
                break
        if found:
            pdf.screenshot(found.name)
        else:
            pdf.note_text(
                "Pending the Render deployment described in DEPLOYMENT.md - this screenshot "
                "will be captured against the live URL once it's available."
            )

    out_path = ROOT / "submission.pdf"
    pdf.output(str(out_path))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    build()
