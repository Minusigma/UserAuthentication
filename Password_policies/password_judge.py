
"""
Judge the passwords' stength by methods from esay to hard.
"""
class Judge:
    def __init__(self,password):
        self.password = password

    def judge(self):
        """
        Handle methods to judge the password.
        : return: the strenth number of password, 0 if the password is invalid under this method, 5 if the password is strong enough.
        """
        return NotImplemented
    
    def _3_class_8(self):
        """
        The password must contain at least 1 lower-case letter, 1 upper-case letter and 1 specific symbol.
        : return: the strenth of password.
        """

        return NotImplemented
    
    def most_used_filter(self):
        """
        It will search for the database of 100k-most-used-password-NCSC to avoid the most common passwords.
        : return: True if not find in database.
        """

        return NotImplemented

    def PGS(self):
        """
        Use the Password Guessability Service (PGS) to guess the password. The trial will dispaly the strenth of the password.
        : return: the strenth of password.
        """
        return NotImplemented
    
    def display(self):
        """
        To show the strenth of password.
        """

        return
def main():
    word = ''
    while word != 'quit':
        word = input("Please write your password (type 'quit' to leave): ")
        Judge(word).judge()


if __name__ == "__main__":
    main()