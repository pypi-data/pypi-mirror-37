from setuptools import setup

setup(
    name="aileen",
    description="The Aileen project - A data-driven service layer for Humanitarian Aid",
    author="Seita BV, PNGK BV",
    author_email="nicolas@seita.nl",
    keywords=[],
    version="0.1.2",
    # flask should be after all the flask plugins, because setup might find they ARE flask
    install_requires=[
        "isodate",
        "pytz",
        "tzlocal",
        "click",
        "python-dotenv",
        "libtmux",
        "watchdog",
        "netifaces",
        "pandas",
        "pexpect",
        "inflection",
        "humanize",
        "Flask-SSLify",
        "Flask_JSON",
        "Flask-SQLALchemy",
        "psycopg2-binary",
        "Flask-Migrate",
        "Flask-Marshmallow",
        "flask>=1.0",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-flask", "requests"],
    packages=["aileen"],
    include_package_data=True,
    # license="Apache",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    scripts=["aileen/scripts/aileen-start-suite", "aileen/scripts/aileen"],
    long_description="""\
            Humanitarian Aid wants to count beneficiaries for the purposes of capacity planning. The Aileen package
            wants to help automate counting of attendance by looking at Wifi traffic.
""",
)
