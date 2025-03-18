"""
Setup script for the wingman package.
"""
from setuptools import setup, find_packages

setup(
    name="wingman",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.28.5",
        "pyyaml>=6.0.1",
        "langchain>=0.0.335",
        "langchain-openai>=0.0.5",
        "openai>=1.10.0",
    ],
    author="Wingman Team",
    author_email="info@wingman.ai",
    description="Agentic architecture using CrewAI",
    keywords="ai, agents, crewai",
    python_requires=">=3.8",
)
