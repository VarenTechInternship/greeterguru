import requests as req
import ldap
from django_auth_ldap.backend import LDAPBackend


def populate():

    host = "192.168.200.128"		   # Server’s name/IP address
    username = "internship\\Administrator" # Any user’s login name on the server
    password  = "V@r3nTech#"		   # The user’s password
    
    # Connect to active directory and bind as a user
    conn = ldap.initialize("ldap://" + host)
    conn.simple_bind_s(username, password)
    
    domain = "cn=Users,dc=internship,dc=com" # Where to look in active directory
    searchFilter = "(ou=Employee)"    # Entries to look for
    attributes = ["sAMAccountName"]   # Info to return about found entries

    # Retrieve specified entries and information
    resultID = conn.search(domain, ldap.SCOPE_SUBTREE, searchFilter, attributes)
    # Retrieve first entry
    entry = conn.result(resultID, 0)[1]
    
    results = [] 	# Stores all usernames
    # Iterate through returned entries and compile all usernames
    while (entry != []):
        # Extract username of current entry and add it to list
        results.append(entry[0][1]["sAMAccountName"][0].decode("utf-8"))
        # Retrieve next entry
        entry = conn.result(resultID, 0)[1]

    # Populate database with users
    for username in results:
        user = LDAPBackend().populate_user(username=username)
        if user is None:
            raise Exception("No User name {}".format(username))

    url = "http://localhost:8000/api/"
    employees = req.get(url + "employees/").json()
    for emp in employees:
        if emp["username"] not in results and not emp["database_only"]:
            response = req.delete(url + "employees/" + str(emp["emp_ID"]) + "/")
