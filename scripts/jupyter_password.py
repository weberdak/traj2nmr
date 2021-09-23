from notebook.auth import passwd
from sys import argv

# Run in Unix shell
# $ python3 jupyter_password.py <password>
# Ouputs hashed password

def main():
	"""Print hashed password from input string to terminal"""
	passwd_in = str(argv[1])
	passwd_hash = passwd(passwd_in)
	print(passwd_hash)

if __name__ == '__main__':
    main()