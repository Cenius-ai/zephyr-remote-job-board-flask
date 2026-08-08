"""API endpoints for jobs, companies, and tags (JSON responses)."""

from flask import Blueprint, jsonify, request

from models import Job, Tag, db
from services.filter_service import build_job_query

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/jobs")
def list_jobs():
    """Return filtered, paginated job list as JSON."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)

    # Clamp pagination bounds
    page = max(1, page)
    per_page = max(1, min(per_page, 50))

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

    return jsonify({
        "jobs": [job.to_dict() for job in pagination.items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    })


@api_bp.route("/jobs/<int:job_id>")
def get_job(job_id):
    """Return a single job by ID with tags."""
    job = db.session.get(Job, job_id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job.to_dict())


@api_bp.route("/companies")
def list_companies():
    """Return distinct company names."""
    rows = db.session.query(Job.company).distinct().order_by(Job.company).all()
    return jsonify([r[0] for r in rows])


@api_bp.route("/tags")
def list_tags():
    """Return all tag names."""
    rows = Tag.query.order_by(Tag.name).all()
    return jsonify([t.name for t in rows])
