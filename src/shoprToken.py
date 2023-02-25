import jwt

shoprTokenSecret = "theMostSecretCodeEver"

def tokenNew(userID):
    return jwt.encode(payload={
        "userID": userID
    },
    key=shoprTokenSecret)
    
def tokenDecrypt(token):
    headerData = jwt.get_unverified_header(token)
    return jwt.decode(token, shoprTokenSecret, algorithms=[headerData['alg']])

