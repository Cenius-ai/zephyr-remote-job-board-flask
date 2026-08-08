from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Many-to-many association table for jobs <-> tags
job_tag = db.Table(
    "job_tag",
    db.Column("job_id", db.Integer, db.ForeignKey("job.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    remote_type = db.Column(db.String(50), nullable=False)  # remote, on-site, hybrid
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    posted_date = db.Column(db.Date, default=date.today, nullable=False)
    apply_url = db.Column(db.String(500), nullable=True)

    tags = db.relationship("Tag", secondary=job_tag, back_populates="jobs")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "remote_type": self.remote_type,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "apply_url": self.apply_url,
            "tags": [t.name for t in self.tags],
        }


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    jobs = db.relationship("Job", secondary=job_tag, back_populates="tags")
