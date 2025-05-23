import setuptools
import os

# Function to read requirements from a file
def parse_requirements(filename):
    """load requirements from a pip requirements file, excluding git+ dependencies"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#") and not line.startswith("git+")]

# Read the contents of your README file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get regular requirements from requirements.txt (excluding git+ dependencies)
install_requires = parse_requirements(os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt"))
# Remove setuptools if present, as it's a build dependency
install_requires = [req for req in install_requires if 'setuptools' not in req.lower()]
# Remove torch and torchvision to avoid version conflicts - assume they're already installed
install_requires = [req for req in install_requires if not req.startswith('torch')]

# Process requirements: ensure diffusers[torch] is present
diffusers_handled = False
for i, req in enumerate(install_requires):
    if req.startswith('diffusers'):
        install_requires[i] = 'diffusers[torch]'
        diffusers_handled = True
        break

if not diffusers_handled:
    install_requires.append('diffusers[torch]')

# Add local sub-packages
install_requires.extend([
    "segment_anything @ file://" + os.path.abspath(os.path.join(os.path.dirname(__file__), "segment_anything")),
    "groundingdino @ file://" + os.path.abspath(os.path.join(os.path.dirname(__file__), "GroundingDINO")),
])

setuptools.setup(
    name="grounded_segment_anything",
    version="0.1.0",
    author="Grounded-SAM Contributors",
    author_email="contact@idea.edu.cn",
    description="Grounded-Segment-Anything: Detect and segment anything with text inputs!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IDEA-Research/Grounded-Segment-Anything",
    packages=setuptools.find_packages(exclude=["outputs*", "assets*", "playground*", "*.tests", "*.tests.*", "tests.*", "tests", "docs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=install_requires,
)