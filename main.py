import random
import string
import sys

from PyQt6.QtWidgets import QDialog, QApplication

from layout import Ui_Dialog
COMPLETED_STYLE = """
QProgressBar{
    border-radius: 10px;
    text-align: center
}

QProgressBar::chunk {
    border-radius: 10px;
    background-color: red;
}
"""


COMPLETED_STYLE2 = """
QProgressBar{
    border-radius: 10px;
    text-align: center
}

QProgressBar::chunk {
    border-radius: 10px;
    background-color: yellow;
}
"""


COMPLETED_STYLE3 = """
QProgressBar{
    border-radius: 10px;
    text-align: center
}

QProgressBar::chunk {
    border-radius: 10px;
    background-color: green;
}
"""

class MyForm(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.easter.clicked.connect(self.easterClicked)
        self.ui.password.textChanged.connect(self.checkPassword)
        self.ui.passwordPower.setStyleSheet(COMPLETED_STYLE)
        self.checklist = {'small': 0, 'large': 0, 'numbers': 0, 'specialchars': 0, 'checkWord': 0}
        self.score = 0
        self.lenPkt = 0

        #zasobnik znakow
        self.smallChars = [l for l in string.ascii_lowercase]
        self.capitalChars = [l for l in string.ascii_uppercase]
        self.numbers = [str(i) for i in range(0,10)]
        self.specialChars = [l for l in string.punctuation]


    def generate(self):
        length = self.ui.passwordLength.text()
        type = self.ui.passwordType.currentText()
        pasword = ''
        if type == 'Pin':
            for i in range(int(length)):
                pasword += str(random.randint(0,9))
        elif self.ui.word.isChecked():
            words = self.readDict('odm.txt')
            while len(pasword) < int(length):
                pasword += random.choice(words)
        else:
            elements = [self.smallChars]
            if self.ui.specialChar.isChecked():
                elements.append(self.specialChars)
            if self.ui.numbers.isChecked():
                elements.append(self.numbers)
            if self.ui.capitalChars.isChecked():
                elements.append(self.capitalChars)

            for i in range(int(length)):
                type = random.randint(0, len(elements)-1)
                pasword += elements[type][random.randint(0, len(elements[type])-1)]

            if self.ui.easter.isChecked() and len(pasword) >= 5:
                max_index = len(pasword) - 6
                start_index = random.randint(0,max_index)
                new_pasword = ''
                easter = 'zając'
                for i in range(len(pasword)):
                    if start_index <= i < start_index+5:
                        new_pasword += easter[i - start_index]
                    else:
                        new_pasword += pasword[i]
                pasword = new_pasword

        self.ui.genertedPassword.setText(pasword)


    def readDict(self, path):
        words = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(',')[0]
                line = line.replace('\n','')
                if len(line) > 2 and line.find(' ') == -1:
                    words.append(line)
        return words


    def checkPassword(self):
        password = self.ui.password.text()
        self.test(password)

        if self.score < 50:
            self.ui.passwordPower.setStyleSheet(COMPLETED_STYLE)
        elif self.score < 70:
            self.ui.passwordPower.setStyleSheet(COMPLETED_STYLE2)
        else:
            self.ui.passwordPower.setStyleSheet(COMPLETED_STYLE3)

        self.ui.passwordPower.setValue(self.score)
        print(self.score)



    def test(self, password):
        self.score = 0
        for x in self.checklist:
            self.checklist[x] = 0
        if any(char.islower() for char in password):
            self.checklist['small'] += 10
        if any(char.isupper() for char in password):
            self.checklist['large'] += 10
        if any(char.isdigit() for char in password):
            self.checklist['numbers'] += 12
        if any(char in string.punctuation for char in password):
            self.checklist['specialchars'] += 12
        if self.sprawdz_wyraz_w_pliku(password, './listaHasel.txt'):
            self.checklist['checkWord'] -= 20
        if len(password) >= 1:
            self.lenPkt = 5 * (len(password))
            self.score += self.lenPkt
            self.lenPkt = 0
        for x in self.checklist:
            self.score += self.checklist[x]
        if self.score > 100:
            self.score = 100




    def sprawdz_wyraz_w_pliku(self, wyraz, sciezka_do_pliku):
            with open(sciezka_do_pliku, 'r') as plik:
                for linia in plik:
                    #print(linia)
                    linia = linia.replace('\n','')
                    if wyraz == linia:
                        return True
            return False


    def easterClicked(self):
        if self.ui.easter.isChecked():
            self.ui.numbers.setChecked(False)
            self.ui.capitalChars.setChecked(False)
            self.ui.specialChar.setChecked(False)
            self.ui.word.setChecked(False)
            self.ui.numbers.setDisabled(True)
            self.ui.capitalChars.setDisabled(True)
            self.ui.specialChar.setDisabled(True)
            self.ui.word.setDisabled(True)
        else:
            self.ui.numbers.setDisabled(False)
            self.ui.capitalChars.setDisabled(False)
            self.ui.specialChar.setDisabled(False)
            self.ui.word.setDisabled(False)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()

    sys.exit(app.exec())