### documentation ###
# 1st parameter: postgres password
# 2nd parameter: postgres database
# 3rd parameter: postgres user

# verify service status
sudo systemctl status postgresql

# credentials
password="$1"
[[ -z "$password" ]] && { echo "Database password not found"; exit 1; }

database="$2"
[[ -z "$database" ]] && { echo "Database name not found"; exit 1; }

username="$3"
[[ -z "$username" ]] && { echo "Username for database name not found"; exit 1; }

# setting up
sudo -u postgres createdb "$database"; #create database
sudo -u postgres createuser "$username"; #create username
sudo -u postgres psql -c "ALTER USER $username WITH PASSWORD '$password';" #alter user's password
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $database TO $username;" #grant user's privilege
