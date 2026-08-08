"""Seed the database with 50+ realistic remote tech job listings."""

import random
from datetime import date, timedelta

from app import create_app
from models import Job, Tag, db

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

REMOTE_TYPES = ["remote", "hybrid", "on-site"]

COMPANIES = [
    "Stripe", "Zapier", "GitLab", "Automattic", "Doist", "Buffer",
    "Toptal", "Basecamp", "Shopify", "Hotjar", "InVision", "Close",
    "Linear", "Vercel", "Notion", "Figma", "Airtable", "Supabase",
    "PlanetScale", "Fly.io", "Railway", "Sourcegraph", "Tailscale",
    "HashiCorp", "Datadog", "Twilio", "Cloudflare", "Netlify",
    "Render", "Replit",
]

JOB_TITLES = [
    "Senior Frontend Engineer", "Backend Developer", "Full-Stack Engineer",
    "DevOps Engineer", "Site Reliability Engineer", "Data Engineer",
    "Machine Learning Engineer", "iOS Developer", "Android Developer",
    "Platform Engineer", "Security Engineer", "Engineering Manager",
    "Technical Lead", "Product Engineer", "Infrastructure Engineer",
    "QA Automation Engineer", "API Engineer", "Cloud Architect",
    "Solutions Engineer", "Developer Advocate", "Staff Engineer",
    "Principal Engineer", "Embedded Systems Engineer", "Blockchain Developer",
    "Technical Writer", "UX Engineer", "Data Scientist",
    "Release Engineer", "Build Engineer", "Performance Engineer",
]

JOB_DESCRIPTIONS = [
    (
        "We're looking for a talented engineer to join our distributed team. "
        "You'll work on building and scaling our core platform, collaborating "
        "with designers and product managers to ship features that impact "
        "millions of users. Our stack includes modern technologies and we "
        "emphasize code quality, testing, and continuous delivery.\n\n"
        "What you'll do:\n"
        "- Design, build, and maintain APIs and services\n"
        "- Collaborate with cross-functional teams to define and ship features\n"
        "- Write clean, well-tested, and documented code\n"
        "- Participate in code reviews and mentor junior engineers\n"
        "- Contribute to architectural decisions and technical strategy\n\n"
        "We value work-life balance and offer flexible hours. You'll have the "
        "autonomy to make decisions and the support to grow your career."
    ),
    (
        "Join our engineering team to help build the next generation of our "
        "product. We're a remote-first company with team members across 20+ "
        "countries. You'll own features from conception to deployment, working "
        "with a stack that includes modern web frameworks and cloud services.\n\n"
        "Key responsibilities:\n"
        "- Develop new features and improve existing ones\n"
        "- Optimize application performance and reliability\n"
        "- Write automated tests and maintain CI/CD pipelines\n"
        "- Troubleshoot production issues and participate in on-call rotation\n"
        "- Document technical designs and contribute to RFCs\n\n"
        "We offer competitive compensation, equity, and a home office stipend. "
        "Our async-first culture means you control your schedule."
    ),
    (
        "We're a fast-growing startup building tools that developers love. "
        "Our small, senior team values craftsmanship, ownership, and simplicity. "
        "You'll have outsized impact from day one, working directly with "
        "founders and shaping both the product and the engineering culture.\n\n"
        "You will:\n"
        "- Ship features end-to-end across the full stack\n"
        "- Make pragmatic technical decisions with long-term thinking\n"
        "- Build internal tools and automation to keep us moving fast\n"
        "- Engage with our developer community and incorporate feedback\n"
        "- Help us scale from thousands to millions of users\n\n"
        "We believe in transparency, async communication, and written culture. "
        "Every team member gets meaningful equity and the tools they need."
    ),
    (
        "We're seeking an experienced engineer to join our platform team. "
        "You'll work on the infrastructure that powers our products, ensuring "
        "reliability, scalability, and developer productivity. This role is "
        "ideal for someone who enjoys solving complex distributed systems "
        "problems and building tools that multiply team output.\n\n"
        "What you'll work on:\n"
        "- Design and implement scalable backend services\n"
        "- Build internal developer platforms and tooling\n"
        "- Improve observability, monitoring, and alerting\n"
        "- Optimize database performance and query patterns\n"
        "- Lead incident response and postmortem processes\n\n"
        "We invest heavily in our platform engineering culture. You'll have "
        "dedicated time for learning, experimentation, and open-source contributions."
    ),
    (
        "Come build the future of work with us. We're reimagining how teams "
        "collaborate across time zones, and we need engineers who care deeply "
        "about craft and user experience. Our product serves teams from startups "
        "to Fortune 500 companies.\n\n"
        "Day to day:\n"
        "- Partner with product and design to spec out new features\n"
        "- Build responsive, accessible user interfaces\n"
        "- Evolve our API design and data models\n"
        "- Improve test coverage and refactor legacy code\n"
        "- Share knowledge through docs, talks, and mentoring\n\n"
        "We're profitable, growing, and committed to building a diverse, "
        "inclusive team. Benefits include unlimited PTO, health coverage, "
        "and annual team retreats."
    ),
]


def seed_tags():
    """Create all predefined tech tags."""
    created = 0
    for tag_name in TECH_TAGS:
        existing = Tag.query.filter_by(name=tag_name).first()
        if not existing:
            db.session.add(Tag(name=tag_name))
            created += 1
    db.session.commit()
    return created


def seed_jobs(count=55):
    """Create demo job listings with realistic data."""
    random.seed(42)

    all_tags = Tag.query.all()
    if not all_tags:
        raise RuntimeError("No tags found — run seed_tags() first.")

    created = 0
    today = date.today()

    for i in range(count):
        title = JOB_TITLES[i % len(JOB_TITLES)]
        if i >= len(JOB_TITLES):
            suffix_num = (i // len(JOB_TITLES)) + 1
            title = f"{title} {suffix_num}"

        company = COMPANIES[i % len(COMPANIES)]
        remote_type = REMOTE_TYPES[i % len(REMOTE_TYPES)]
        desc_variant = JOB_DESCRIPTIONS[i % len(JOB_DESCRIPTIONS)]

        # Realistic salary ranges
        if i % 5 == 0:
            salary_min, salary_max = None, None
        else:
            base = random.choice([80_000, 100_000, 120_000, 140_000, 160_000, 180_000, 200_000])
            salary_min = base + random.randint(0, 20_000)
            salary_max = salary_min + random.choice([20_000, 30_000, 40_000, 50_000, 60_000])

        days_ago = random.randint(0, 30)
        posted = today - timedelta(days=days_ago)

        apply_url = None
        if i % 3 != 0:
            apply_url = f"https://{company.lower().replace(' ', '')}.com/careers/{i + 100}"

        job = Job(
            title=title,
            company=company,
            description=desc_variant,
            remote_type=remote_type,
            salary_min=salary_min,
            salary_max=salary_max,
            posted_date=posted,
            apply_url=apply_url,
        )

        num_tags = random.randint(3, 6)
        chosen_tags = random.sample(all_tags, num_tags)
        job.tags.extend(chosen_tags)

        db.session.add(job)
        created += 1

    db.session.commit()
    return created


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        tags_created = seed_tags()
        print(f"Created {tags_created} new tags (total: {Tag.query.count()})")

        existing_count = Job.query.count()
        if existing_count >= 55:
            print(f"Database already has {existing_count} jobs — skipping seed.")
        else:
            to_create = 55 - existing_count
            jobs_created = seed_jobs(to_create)
            print(f"Created {jobs_created} jobs (total: {Job.query.count()})")

        print("Seed complete.")


if __name__ == "__main__":
    main()
