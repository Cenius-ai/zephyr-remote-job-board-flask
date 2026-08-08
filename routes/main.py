"""HTML page routes: home (job list), job detail, about, hello."""

from flask import Blueprint, render_template, request, abort

from models import Job, db
from services.filter_service import build_job_query

main_bp = Blueprint("main", __name__)


@main_bp.route("/hello")
def hello():
    """T1 sanity-check placeholder route."""
    return "Hello"


@main_bp.route("/")
def index():
    """Job listing page with filters."""
    page = request.args.get("page", 1, type=int)
    per_page = 12
    page = max(1, page)

    # Capture filter params for template context
    filters = {
        "title": request.args.get("title", ""),
        "company": request.args.get("company", ""),
        "tech_stack": request.args.get("tech_stack", ""),
        "remote_type": request.args.get("remote_type", ""),
        "salary_min": request.args.get("salary_min", ""),
        "salary_max": request.args.get("salary_max", ""),
    }

    query = build_job_query(
        title=request.args.get("title"),
        company=request.args.get("company"),
        tech_stack=request.args.get("tech_stack"),
        remote_type=request.args.get("remote_type"),
        salary_min=request.args.get("salary_min", type=int),
        salary_max=request.args.get("salary_max", type=int),
    )

    pagination = query.order_by(Job.posted_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Preload filter options
    companies = sorted(
        [r[0] for r in db.session.query(Job.company).distinct().all()]
    )
    from models import Tag
    tags_list = sorted(
        [t.name for t in Tag.query.order_by(Tag.name).all()]
    )

    return render_template(
        "index.html",
        jobs=pagination.items,
        page=pagination.page,
        pages=pagination.pages,
        total=pagination.total,
        filters=filters,
        companies=companies,
        tags_list=tags_list,
    )


@main_bp.route("/jobs/<int:job_id>")
def job_detail(job_id):
    """Single job detail page."""
    job = db.session.get(Job, job_id)
    if job is None:
        abort(404)
    return render_template("job_detail.html", job=job)


@main_bp.route("/about")
def about():
    """About page."""
    return render_template("about.html")
