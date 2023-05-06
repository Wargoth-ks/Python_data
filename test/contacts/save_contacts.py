import atexit
import pickle
import os

FILENAME = 'contacts.pickle'

# Save contacts on exit


def save_contacts_on_exit():
    with open(FILENAME, 'wb') as f:
        pickle.dump(contacts, f)

# Load contacts


if os.path.exists(FILENAME):
    with open(FILENAME, 'rb') as f:
        contacts = pickle.load(f)
else:
    contacts = {}

# Registration of a function for saving contacts when the program is finished
atexit.register(save_contacts_on_exit)
