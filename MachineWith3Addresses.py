from tkinter.tix import *
import math


class Machine3:
    def __init__(self, locations):
        self.__date = locations
        self.__code = ''
        self.__address1 = ''
        self.__address2 = ''
        self.__address3 = ''

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value

    @property
    def address1(self):
        return self.__address1

    @address1.setter
    def address1(self, value):
        self.__address1 = value

    @property
    def address2(self):
        return self.__address2

    @address2.setter
    def address2(self, value):
        self.__address2 = value

    @property
    def address3(self):
        return self.__address3

    @address3.setter
    def address3(self, value):
        self.__address3 = value

    def execute(self, console):
        if self.code == '+':
            self.date[self.address3] = self.date[self.address1] + self.date[self.address2]
        elif self.code == '-':
            self.date[self.address3] = self.date[self.address1] - self.date[self.address2]
        elif self.code == '*':
            self.date[self.address3] = self.date[self.address1] * self.date[self.address2]
        elif self.code == '/':
            self.date[self.address3] = self.date[self.address1] / self.date[self.address2]
        elif self.code == 'sqrt':
            self.date[self.address3] = math.sqrt(self.date[self.address1])
        elif self.code == 'abs':
            self.date[self.address3] = abs(self.date[self.address1])
        elif self.code == 'int':
            self.date[self.address3] = int(self.date[self.address1])
        elif self.code == 'SN':
            self.start(console, self.address3)
            return 0
        elif self.code == '<':
            if self.date[self.address1] < self.date[self.address2]:
                self.start(console, self.address3)
                return 0
        elif self.code == '<=':
            if self.date[self.address1] <= self.date[self.address2]:
                self.start(console, self.address3)
                return 0
        elif self.code == '>':
            if self.date[self.address1] > self.date[self.address2]:
                self.start(console, self.address3)
                return 0
        elif self.code == '>=':
            if self.date[self.address1] >= self.date[self.address2]:
                self.start(console, self.address3)
                return 0
        elif self.code == '==':
            if self.date[self.address1] == self.date[self.address2]:
                self.start(console, self.address3)
                return 0
        elif self.code == '!=':
            if self.date[self.address1] != self.date[self.address2]:
                self.start(console, self.address3)
                return 0
        elif self.code == 'WRITE':
            label_text = self.address3 + ": " + str(self.date[self.address3])
            Label(console, text=label_text, font=(None, 10, "bold")).pack()
        elif self.code == 'STOP':
            Label(console, text="").pack()
            Label(console, text="The program execution finished successfully!", font=(None, 10)).pack()
            Label(console, text='aka "Good job! You emulated the functioning of a computer processor!" :)', font=(None, 10, "bold")).pack()
            Label(console, text="").pack()

    def enter(self, console, text, addresses, button):
        label_text = "Read " + addresses[0] + ": "
        Label(console, text=label_text, font=(None, 10)).pack()

        entry = Text(console, height=1, width=10)
        entry.pack()
        button1 = Button(console, text="Send", font=(None, 10), bg="lightblue")
        button1.pack()
        address = addresses[0]
        button1.bind("<Button-1>",
                     lambda event, _console=console, _entry=entry, _address=address: self.read(console, entry, address))

        Label(console, text="").pack()
        del addresses[0]
        if len(addresses) == 0:
            button.config(bg="lightgray", state=DISABLED)
            button.unbind("<Button-1>")

            button2 = Button(console, text="Get the result!", font=(None, 10, "bold"), bg="skyblue")
            button2.pack()
            button2.bind("<Button-1>", lambda event, _console=console, _text=text: self.go_on(console, text))

            Label(console, text="").pack()

    def read(self, console, entry, address):
        try:
            self.date[address] = int(entry.get("1.0", "end-1c"))
            entry.config(fg="darkgreen", font=("courier", 10, "bold"))

        except ValueError:
            entry.config(fg="red")
            Label(console, text="Please, I work with numbers!", font=(None, 10), fg="red").pack()
            Label(console, text="").pack()

    def go_on(self, console, text):
        try:
            for line in text.strip().split('\n'):
                self.code, self.address1, self.address2, self.address3 = line.strip().split(' ')
                if self.code != 'READ':
                    if '+' in self.address1:
                        x, index = self.address1.split('+')
                        self.address1 = x + '+' + str(self.date['I'])

                    if '+' in self.address2:
                        x, index = self.address2.split('+')
                        self.address2 = x + '+' + str(self.date['I'])

                    if '+' in self.address3:
                        x, index = self.address3.split('+')
                        self.address3 = x + '+' + str(self.date['I'])

                    if self.execute(console) == 0:
                        break

        except Exception as e:
            Label(console, text="Something's not good. We have an error:", font=(None, 10), fg="red").pack()
            error = type(e).__name__ + ": " + str(e)
            Label(console, text=error, font=(None, 10, "italic"), fg="red").pack()
            Label(console, text="").pack()
            raise

    def start(self, console, file_name):
        Label(console, text="").pack()

        file = open(file_name + '.txt', 'r')
        text = file.read()
        file.close()

        to_read = []
        for line in text.strip().split('\n'):
            self.code, self.address1, self.address2, self.address3 = line.strip().split(' ')

            if self.code == 'READ':
                if '+' in self.address3:
                    x, index = self.address3.split('+')
                    self.address3 = x + '+' + str(self.date['I'])

                to_read.append(self.address3)

        if len(to_read) != 0:
            button = Button(console, text="Read a value", font=(None, 10, "bold"), bg="skyblue")
            button.pack()
            button.bind("<Button-1>",
                        lambda event, _console=console, _text=text, _addresses=to_read, _button=button:
                        self.enter(console, text, to_read, button))

            Label(console, text="").pack()

        else:
            self.go_on(console, text)
