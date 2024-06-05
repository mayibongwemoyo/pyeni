from setuptools import setup, find_packages

setup(
    name='pyeni',
    version='0.1.0',  # Adjust version number
    description='Alternative monitoring interface for ENM',
    author='Your Name',
    author_email='your_email@example.com',
    packages=find_packages(),
    install_requires=[
        'paramiko',
        'python-dotenv',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'pyeni = pyeni:main',  # Optional: Define a command-line entry point
        ],
    },
    packages=find_packages(),
    # ... (rest of setup.py settings)
)