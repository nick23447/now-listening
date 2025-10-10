from setuptools import setup, find_packages

setup(
    name='musicblog',
    version='0.1.0',
    description='A music blog application built with Flask',
    packages=find_packages(),
    install_requires=[
        'flask>=3.0.0',
        'flask-sqlalchemy>=3.0.0',
        'flask-bcrypt>=1.0.0',
        'flask-login>=0.6.0',
        'flask-migrate>=4.0.0',
        'flask-wtf>=1.2.0',
        'email-validator>=2.0.0',
        'pillow>=11.0.0',
        'requests>=2.32.0',        # For API calls (Spotify, etc.)
    ],
    extras_require={
        'dev': [
            'pytest>=8.0.0',
            'pytest-mock>=3.14.0',
            'pytest-cov>=4.0.0',   # Better than coverage directly
        ]
    },
    python_requires='>=3.8',
)