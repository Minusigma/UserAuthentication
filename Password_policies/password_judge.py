import re
import psycopg2
import zxcvbn

"""
Judge the passwords' stength by methods from esay to hard.
"""
class Judge:
    def __init__(self,password = '') -> None:
        self.password = password

    def judge(self) -> int:
        """
        Handle methods to judge the password.
        : return: the strenth number of password, 0 if the password is invalid under this method, 5 if the password is strong enough.
        """
        s_level = self._3_class_8()
        self.print(s_level)
        return s_level
    
    def _3_class_8(self):
        """
        The password must contain at least 1 lower-case letter, 1 upper-case letter and 1 number.
        : return: the strenth of password.
        """
        ######################
        # [-----] No password or password is invalid
        # [=----] Too Weak
        # [==---] Weak
        # [===--] Normal
        # [====-] Good
        # [=====] Perfect
        ######################
        password = self.password

        specific_symbol = re.compile(r".*[\(\)`!@#\$%^&\*_\-+=|{}\[\]:;'<>,\.\?/].*")
        number = re.compile(r'.*[0-9].*')
        lower_case_letter = re.compile(r'.*[a-z].*')
        upper_case_letter = re.compile(r'.*[A-Z].*')
        all_satisfied = re.compile(r"[\(\)`!@#\$%^&\*_\-+=|{}\[\]:;'<>,\.\?/0-9a-zA-Z]")
        
        secure_level = 0
        msg = ''

        if len(password) == 0:
            secure_level = 0
            msg = 'Password is empty.'
        elif len(password.split(" ")) != 1 or len(password.split(" ")[0]) == 0:
            secure_level = 0
            msg = 'Password should not countain space.'
        elif len(password) < 8:
            secure_level = 0
            msg = 'Password is too short.'
        elif len(all_satisfied.findall(password)) < len(password):
            secure_level = 0
            msg = 'Invalid password.'
        else:
            if lower_case_letter.match(password):
                secure_level += 1
            if upper_case_letter.match(password):
                secure_level += 1
            if number.match(password):
                secure_level += 1
            if specific_symbol.match(password):
                secure_level += 1
            if len(password) > 14:
                secure_level += 1
        print(msg)
        return secure_level
    
    def most_used_filter(self):
        """
        It will search for the database of 100k-most-used-password-NCSC to avoid the most common passwords.
        : return: True if not find in database.
        """
        with open('100k-most-used-passwords-NCSC.txt', 'r') as file:
            most_used_passwords = file.read().splitlines()
        if self.password in most_used_passwords:
            return False
        return True

    def zxcvbn_meter(self):
        """
        Use the zxcvbn to estimate the strenth of password. The trial will dispaly the strenth of the password.
        : return: the strenth of password.
        """
        strenth = zxcvbn.password_strength(self.password)
        return NotImplemented
    
    def display(self):
        """
        To show the strenth of password.
        """

        return
    
    def print(self, secure_level):
        if secure_level == 0:
            print('[-----] No password or password is invalid')
        elif secure_level == 1:
            print('[=----] Too Weak')
        elif secure_level == 2:
            print('[==---] Weak')
        elif secure_level == 3:
            print('[===--] Normal')
        elif secure_level == 4:
            print('[====-] Good')
        elif secure_level == 5:
            print('[=====] Perfect')
        else:
            print('invalid secure_level')

def main():
    while True:
        word = input("Please write your password (type 'quit' to leave): ")
        if word == 'quit':
            break
        Judge(word).judge()


if __name__ == "__main__":
    main()