from tkinter.tix import *
import math


class Machine1:
    __instructions = {1: '<-', 2: '->', 3: '<-I', 4: '->I', 5: '<-B', 6: '->B', 7: '|vX', 8: '|^X', 9: '|v', 10: '|^',
                      11: '+', 12: '-', 13: '*', 14: '/', 15: 'sqrt', 16: 'abs', 17: 'int', 18: 'SN', 19: '<', 20: '<=',
                      21: '>', 22: '>=', 23: '==', 24: '!=', 25: 'ADR', 26: 'READ', 27: 'WRITE', 28: 'STOP'}

    def __init__(self, locations):
        self.__reg_a = 0
        self.__reg_i = 0
        self.__reg_b = 0
        self.__date = locations
        self.__code = ''
        self.__address = ''
        self.__stack = []

    @property
    def instructions(self):
        return self.__instructions

    @property
    def reg_a(self):
        return self.__reg_a

    @reg_a.setter
    def reg_a(self, value):
        self.__reg_a = value

    @property
    def reg_i(self):
        return self.__reg_i

    @reg_i.setter
    def reg_i(self, value):
        self.__reg_i = value

    @property
    def reg_b(self):
        return self.__reg_b

    @reg_b.setter
    def reg_b(self, value):
        self.__reg_b = value

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
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, value):
        self.__stack = value

    def execute(self, console):
        if self.code == '<-':
            self.reg_a = self.date[self.address]
        elif self.code == '->':
            self.date[self.address] = self.reg_a
        elif self.code == '<-I':
            self.reg_a = self.reg_i
        elif self.code == '->I':
            self.reg_i = self.reg_a
        elif self.code == '<-B':
            self.reg_a = self.reg_b
        elif self.code == '->B':
            self.reg_b = self.reg_a
        elif self.code == '|vX':
            self.stack.append(self.date[self.address])
        elif self.code == '|^X':
            self.date[self.address] = self.stack.pop()
        elif self.code == '|v':
            self.stack.append(self.reg_a)
        elif self.code == '|^':
            self.reg_a = self.stack.pop()

        elif self.code == '+':
            self.reg_a += self.date[self.address]
        elif self.code == '-':
            self.reg_a -= self.date[self.address]
        elif self.code == '*':
            self.reg_a *= self.date[self.address]
        elif self.code == '/':
            self.reg_a /= self.date[self.address]
        elif self.code == 'sqrt':
            self.reg_a = math.sqrt(self.date[self.address])
        elif self.code == 'abs':
            self.reg_a = abs(self.date[self.address])
        elif self.code == 'int':
            self.reg_a = int(self.date[self.address])

        elif self.code == 'SN':
            self.start(console, self.address)
            return 0
        elif self.code == '<':
            if self.reg_a < 0:
                self.start(console, self.address)
                return 0
        elif self.code == '<=':
            if self.reg_a <= 0:
                self.start(console, self.address)
                return 0
        elif self.code == '>':
            if self.reg_a > 0:
                self.start(console, self.address)
                return 0
        elif self.code == '>=':
            if self.reg_a >= 0:
                self.start(console, self.address)
                return 0
        elif self.code == '==':
            if self.reg_a == 0:
                self.start(console, self.address)
                return 0
        elif self.code == '!=':
            if self.reg_a != 0:
                self.start(console, self.address)
                return 0

        elif self.code == 'ADR':
            self.reg_a = self.address
        elif self.code == 'WRITE':
            label_text = self.address + ": " + str(self.date[self.address])
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
                nb, self.address = line.strip().split(' ')
                self.code = self.instructions[int(nb)]

                if self.code != 'READ':
                    try:
                        val = int(self.address)
                        self.date[self.address] = val
                    except ValueError:
                        if '+' in self.address:
                            x, index = self.address.split('+')
                            self.address = x + '+' + str(self.reg_i)

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
            nb, self.address = line.strip().split(' ')
            self.code = self.instructions[int(nb)]

            if self.code == 'READ':
                if '+' in self.address:
                    x, index = self.address.split('+')
                    self.address = x + '+' + str(self.reg_i)

                to_read.append(self.address)

        if len(to_read) != 0:
            button = Button(console, text="Read a value", font=(None, 10, "bold"), bg="skyblue")
            button.pack()
            button.bind("<Button-1>",
                        lambda event, _console=console, _text=text, addresses=to_read, _button=button:
                        self.enter(console, text, to_read, button))

            Label(console, text="").pack()

        else:
            self.go_on(console, text)
