from passlib.context import CryptContext
encrypt= CryptContext(schemes=["bcrypt"], deprecated= "auto")
class Hash:
    def hash(password):
        return encrypt.hash(password)
    def verify(plain_pass,hash_pass):
        return encrypt.verify(plain_pass,hash_pass)