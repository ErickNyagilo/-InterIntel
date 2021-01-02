import bcrypt 

password = b"qwerty12"  

hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)

"""
    Get username and password from a form using Flask and encode it before hashing
"""

# username =  request.form.get("username")
# password = request.form.get("password").encode("utf-8")



# looking user up in DB username
if bcrypt.checkpw(password, hashed):
    print("It matches!")
else: 
    print("Didn't match")
