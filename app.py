"""Zephyr — Remote Tech Job Board (Flask application entrypoint)."""

import os

from flask import Flask

from config import Config
from models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(_e):
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        from flask import render_template
        return render_template("500.html"), 500

    # Auto-create tables + seed on first boot (idempotent)
    with app.app_context():
        db.create_all()
        _seed_if_empty()

    return app


def _seed_if_empty():
    """Idempotently seed the database if no jobs exist."""
    from models import Job, Tag, db as _db

    if Job.query.first() is not None:
        return

    TECH_TAGS = [
        "Python", "JavaScript", "TypeScript", "React", "Vue", "Angular",
        "Node.js", "Django", "Flask", "FastAPI", "Ruby on Rails", "Go",
        "Rust", "Java", "Kotlin", "Swift", "PostgreSQL", "MongoDB",
        "GraphQL", "Docker", "Kubernetes", "AWS", "GCP", "Azure",
        "CI/CD", "Terraform", "Machine Learning", "Data Engineering",
        "DevOps", "iOS", "Android", "Flutter", "React Native",
        "Svelte", "Next.js", "Tailwind CSS", "Redis", "Kafka",
        "Elasticsearch", "gRPC",
    ]

    for tag_name in TECH_TAGS:
        if not Tag.query.filter_by(name=tag_name).first():
            _db.session.add(Tag(name=tag_name))
    _db.session.commit()

    import seed as seed_module
    seed_module.seed_jobs(55)
    _db.session.commit()


# Module-level Flask app instance — used by Flask runner and main.py
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
