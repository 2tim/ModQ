# ModQ
Example code for ModuleQ


## Setup and Installation

1. Clone the repo: `git clone https://github.com/2tim/ModQ.git`
2. Create a virtualenv if necessary using Python 3.5+ (code should run on Python 2.7.x as well but is untested).
3. Install the dependencies for newspaper if not already installed: http://newspaper.readthedocs.io/en/latest/user_guide/install.html
4. Install the packages for the script: `pip install -r requirements.txt`
5. Set the environment variable for the Google cloud api:

    `export GOOGLE_APPLICATION_CREDENTIALS=<insert_path_to_file>/ModQ/MQ\ News\ Matching-2443b471b5ff.json`
6. run the script with `python modq.py`