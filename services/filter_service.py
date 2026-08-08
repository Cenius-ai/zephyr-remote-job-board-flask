"""Build parameterized SQLAlchemy queries from filter parameters.

Injection-safe: all user values are bound as parameters; dynamic columns
would go through an allowlist (not needed here since sort is fixed).
"""

from models import Job, Tag, db


def build_job_query(
    title=None,
    company=None,
    tech_stack=None,
    remote_type=None,
    salary_min=None,
    salary_max=None,
):
    """Return a filtered SQLAlchemy query for Job, with all user values bound.

    Args:
        title: Substring match on job title (LIKE, parameterized).
        company: Exact company name match.
        tech_stack: Comma-separated tag names; jobs must match ALL tags.
        remote_type: One of 'remote', 'on-site', 'hybrid'.
        salary_min: Minimum salary floor (job's salary_max >= this).
        salary_max: Maximum salary ceiling (job's salary_min <= this).

    Returns:
        A SQLAlchemy Query object for Job, ready for further chaining.
    """
    query = Job.query

    if title and title.strip():
        query = query.filter(Job.title.ilike(_like_pattern(title.strip())))

    if company and company.strip():
        query = query.filter(Job.company == company.strip())

    if remote_type and remote_type.strip():
        query = query.filter(Job.remote_type == remote_type.strip())

    if salary_min is not None:
        query = query.filter(
            db.or_(
                Job.salary_max >= salary_min,
                Job.salary_max.is_(None),
            )
        )

    if salary_max is not None:
        query = query.filter(
            db.or_(
                Job.salary_min <= salary_max,
                Job.salary_min.is_(None),
            )
        )

    if tech_stack and tech_stack.strip():
        tag_names = [t.strip() for t in tech_stack.split(",") if t.strip()]
        if tag_names:
            for tag_name in tag_names:
                query = query.filter(
                    Job.tags.any(Tag.name == tag_name)
                )

    return query


def _like_pattern(user_term):
    """Build a safe LIKE pattern from user input.

    Escapes LIKE metacharacters so %, _ in the user term are matched literally,
    then wraps in %wildcards%.
    """
    escaped = user_term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"
