"""
Setup script для my-pentest-gpt
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="my-pentest-gpt",
    version="1.0.0",
    author="Cybersecurity Expert",
    author_email="expert@cybersecurity.com",
    description="AI-инструмент для кибербезопасности на базе DeepSeek-R1-8B",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/my-pentest-gpt",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "gpu": [
            "torch[cuda]>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "my-pentest-gpt=src.cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["prompts/*.json", "data/exploits/*.jsonl"],
    },
    zip_safe=False,
    keywords=[
        "cybersecurity", "pentesting", "ai", "deepseek", "security-tools",
        "ethical-hacking", "vulnerability-assessment", "lora", "machine-learning"
    ],
)
