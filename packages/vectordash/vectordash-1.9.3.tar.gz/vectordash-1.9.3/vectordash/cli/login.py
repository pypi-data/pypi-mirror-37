import click
import os
from colored import fg
from colored import stylize

# getting the base API URL
if os.environ.get('VECTORDASH_BASE_URL'):
    VECTORDASH_URL = os.environ.get('VECTORDASH_BASE_URL')
else:
    VECTORDASH_URL = "https://vectordash.com/"


@click.command(name='login')
def login():
    """
    Stores the user's secret token
    """
    try:
        # defining the dot folder path and token file name
        dot_folder = os.path.expanduser('~/.vectordash/')
        token_path = os.path.join(dot_folder, 'token')

        # ensuring ~/.vectordash/ exists
        if not os.path.isdir(dot_folder):
            os.mkdir(dot_folder)

        print("Your secret key can be found at: {}edit/verification".format(VECTORDASH_URL))
        token = input("Secret: ")

        # writing out the token
        with open(token_path, 'w') as f:
            f.write(str(token))

        print(stylize("Secret successfully updated.", fg("green")))

    except TypeError:
        print(stylize("Error: the provided token was an invalid type.", fg("red")))
