# Emulating the machine with 1/3 addresses

from tkinter.tix import *
import datetime
import glob
import os

from MachineWith3Addresses import Machine3
from MachineWith1Address import Machine1

machine = None
files = []


def choose(var):
    global machine

    if var.get() == 1:
        machine = Machine3({})
    else:
        machine = Machine1({})


def example_m3a(locations, instructions):
    locations.delete(0, END)
    locations.insert(0, "A B C TWO ZERO")

    example = open("example_m3a.txt", 'r')
    text = example.read()
    instructions.delete(1.0, END)
    instructions.insert(1.0, text)
    example.close()


def example_m1a(locations, instructions):
    locations.delete(0, END)
    locations.insert(0, "LA LB LC")

    example = open("example_m1a.txt", 'r')
    text = example.read()
    instructions.delete(1.0, END)
    instructions.insert(1.0, text)
    example.close()


def simulate(main_root, console, locations, instructions):
    if len(locations.get()) == 0 or len(instructions.get("1.0", "end-1c")) == 0:
        Label(console, text="Please, you didn't fill all of the fields.", font=(None, 10), fg="red").pack()
        Label(console, text="").pack()

    else:
        try:
            backups = glob.glob('backup*')
            backup_count = len(backups)

            if backup_count > 0:
                backup = open(backups[backup_count - 1], 'r+')
                line_count = sum(1 for line in backup)
                if line_count >= 100:
                    backup.close()
                    backup_date = "%s" % datetime.date.today()
                    backup_time = "{:%H%M}".format(datetime.datetime.now())
                    backup = open('backup_' + backup_date + '_' + backup_time + '.txt', 'a+')
            else:
                backup_date = "%s" % datetime.date.today()
                backup_time = "{:%H%M}".format(datetime.datetime.now())
                backup = open('backup_' + backup_date + '_' + backup_time + '.txt', 'a+')

            backup.write("Backup: {:%d-%b-%Y %H:%M}".format(datetime.datetime.now()))
            backup.write('\n\n')

            for location in locations.get().strip().split(' '):
                if '+' in location:
                    location = location.split('+')[0] + '+0'
                machine.date[location] = 0

            backup.write("Memory locations (INITIAL stage):\n")
            backup.write(str(machine.date))
            backup.write('\n\n')
            backup.write("Instruction sets:\n")

            for instruction_set in instructions.get("1.0", "end-1c").strip().split('\n\n'):
                file_name = instruction_set.split(':\n')[0] + '.txt'
                files.append(file_name)
                file = open(file_name, 'w')
                file.write(instruction_set.split(':\n')[1])
                file.close()

                backup.write(instruction_set)
                backup.write('\n\n')

            root = Tk()
            root.title("Emulating the machine with 1/3 addresses")
            root.geometry("600x800")
            frame = Frame(root, width=600, height=800)
            frame.pack()
            scrolled_window = ScrolledWindow(frame, width=600, height=800)
            scrolled_window.pack()
            window = scrolled_window.window

            button = console.children["button3"]
            button.bind("<Button-1>", lambda event, root1=main_root, root2=root: restart(main_root, root))

            machine.start(window, files[0].split('.')[0])
            root.mainloop()

            for file in files:
                if os.path.isfile(file):
                    os.remove(file)

            backup.write("Memory locations (FINAL stage):\n")
            backup.write(str(machine.date))
            backup.write('\n\n')
            backup.write('___________________________________________________________\n')
            backup.close()

        except Exception as e:
            Label(console, text="Something's not good. We have an error:", font=(None, 10), fg="red").pack()
            error = type(e).__name__ + ": " + str(e)
            Label(console, text=error, font=(None, 10, "italic"), fg="red").pack()
            Label(console, text="").pack()
            raise


def delete_backups(console):
    try:
        backups = glob.glob('backup*')
        del backups[-1]
        for file in backups:
            os.remove(file)

        Label(console, text="The files were successfully deleted! :)", font=(None, 10)).pack()
        Label(console, text="").pack()

    except Exception as e:
        Label(console, text="Something's not good. We have an error:", font=(None, 10), fg="red").pack()
        error = type(e).__name__ + ": " + str(e)
        Label(console, text=error, font=(None, 10, "italic"), fg="red").pack()
        Label(console, text="").pack()
        raise


def restart(root1, root2):
    if root2 is not None:
        try:
            root2.destroy()
        except tkinter.TclError:
            pass

    root1.destroy()
    main()


def main():
    root = Tk()
    root.iconbitmap(default="processor.ico")
    root.title("Emulating the functioning of a computer processor")
    root.geometry("600x900")

    frame = Frame(root, width=600, height=900)
    frame.pack()
    scrolled_window = ScrolledWindow(frame, width=600, height=900)
    scrolled_window.pack()
    window = scrolled_window.window

    Label(window, text="").pack()

    Label(window, text="Which machine do you want to emulate?", font=(None, 10, "bold")).pack()
    var = IntVar()
    Radiobutton(window, text="The machine with 3 addresses", font=(None, 10), variable=var, value=1,
                command=lambda _var=var: choose(var)).pack()
    Radiobutton(window, text="The machine with 1 address", font=(None, 10), variable=var, value=2,
                command=lambda _var=var: choose(var)).pack()

    Label(window, text="").pack()

    button_eg1 = Button(window, text="Example M3A", font=(None, 10), bg="lightblue")
    button_eg1.place(x=200, y=112)

    button_eg2 = Button(window, text="Example M1A", font=(None, 10), bg="lightblue")
    button_eg2.place(x=305, y=112)

    Label(window, text="").pack()
    Label(window, text="").pack()

    Label(window, text="What memory locations will you use?", font=(None, 10, "bold")).pack()
    entry1 = Entry(window, width=40)
    entry1.pack()

    Label(window, text="").pack()

    Label(window, text="Fill in the instruction sets.", font=(None, 10, "bold")).pack()
    Label(window, text="! The first line of each set represents its label and must be followed by ':' !", font=(None, 10)).pack()
    Label(window, text="! The sets must be separated by a blank line !", font=(None, 10)).pack()
    text = Text(window, height=25, width=50)
    text.pack()

    Label(window, text="").pack()

    button_eg1.bind("<Button-1>", lambda event, console=window, locations=entry1, instructions=text:
                    example_m3a(entry1, text))
    button_eg2.bind("<Button-1>", lambda event, console=window, locations=entry1, instructions=text:
                    example_m1a(entry1, text))

    button1 = Button(window, text="Emulate!", font=(None, 10, "bold"), bg="skyblue")
    button1.pack()
    button1.bind("<Button-1>",
                 lambda event, main_root=root, console=window, locations=entry1, instructions=text:
                 simulate(root, window, entry1, text))

    Label(window, text="").pack()

    button2 = Button(window, text="Delete last backups", font=(None, 10), bg="lightblue")
    button2.pack()
    button2.bind("<Button-1>", lambda event, console=window: delete_backups(window))

    Label(window, text="").pack()

    button3 = Button(window, name="button3", text="Reset the program", font=(None, 10, "bold"), bg="skyblue")
    button3.pack()
    button3.bind("<Button-1>", lambda event, root1=root, root2=None: restart(root, None))

    Label(window, text="").pack()

    root.mainloop()


main()
