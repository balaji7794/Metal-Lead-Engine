from flask import Flask, render_template, request, redirect, jsonify

from src.database.migration import Migration
from src.database.repositories.company_repository import CompanyRepository
from src.database.repositories.email_repository import EmailRepository
from src.database.repositories.phone_repository import PhoneRepository
from src.services.search_manager import search_manager

app = Flask(__name__)

migration = Migration()
migration.run()
migration.close()

@app.route("/")
def dashboard():

    repo = CompanyRepository()

    total_companies = repo.total_companies()

    stats = repo.dashboard_stats()

    companies = repo.get_all()

    repo.close()

    return render_template(

        "dashboard.html",

        total_companies=total_companies,

        companies=companies,

        stats=stats

    )


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

@app.route("/search")
def search():

    return render_template("search.html")


@app.post("/search/start")
def start_search():

    keyword = request.form.get("keyword", "").strip()
    area = request.form.get("area", "").strip()
    city = request.form.get("city", "").strip()
    state = request.form.get("state", "").strip()

    query = keyword

    if area:
        query += f" {area}"

    if city:
        query += f" {city}"

    if state:
        query += f" {state}"

    search_manager.start(query)

    return redirect("/search")


@app.get("/search/status")
def search_status():

    return jsonify(search_manager.status())


# ---------------------------------------------------------
# COMPANIES
# ---------------------------------------------------------

# ---------------------------------------------------------
# COMPANIES
# ---------------------------------------------------------

@app.route("/companies")
def companies():

    keyword = request.args.get("q", "").strip()

    sort = request.args.get("sort", "newest")

    repo = CompanyRepository()

    if keyword:

        companies = repo.search(keyword, sort)

    else:

        companies = repo.get_all(sort)

    repo.close()

    return render_template(

        "companies.html",

        companies=companies,

        keyword=keyword,

        sort=sort

    )


# ---------------------------------------------------------
# COMPANY DETAILS
# ---------------------------------------------------------

@app.route("/company/<int:company_id>")
def company(company_id):

    company_repo = CompanyRepository()
    email_repo = EmailRepository()
    phone_repo = PhoneRepository()

    company = company_repo.get_by_id(company_id)

    emails = email_repo.get_by_company(company_id)

    phones = phone_repo.get_by_company(company_id)

    company_repo.close()
    email_repo.close()
    phone_repo.close()

    return render_template(

        "company.html",

        company=company,

        emails=emails,

        phones=phones

    )


@app.post("/company/<int:company_id>/save")
def save_company(company_id):

    repo = CompanyRepository()

    repo.update_crm(

        company_id,

        request.form.get("lead_status"),

        request.form.get("priority"),

        request.form.get("last_contacted"),

        request.form.get("next_followup"),

        request.form.get("remarks")

    )

    repo.close()

    return redirect(f"/company/{company_id}")


# ---------------------------------------------------------

@app.route("/history")
def history():

    return render_template("history.html")


# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )