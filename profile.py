import os
import time
import tkinter
import tkinter.font
import threading

SLEEP_TIME = 1


class PROFILE_GUI():
    def __init__(self):
        self.__gui = tkinter.Tk()
        self.__labels = []
        self.__errors = []
        self.__entries = []
        self.__errorLabels = []
        # init list of profiles
        self.__prof_list = []
        self.__dict_list = []
        self.__frames = []
        self.__btns = []
        self.__currProf = ""
        self.__textFont = tkinter.font.Font(size=14)
        self.__errFont = tkinter.font.Font(size=12)
        self.__rowCounter = 0
        self.__startPageIdx = 0

        # get current profile from lastProfile.txt
        with open("lastProfile.txt", "r") as read_lp:
            self.__currProf = read_lp.readline()

        # generate list of profiles
        for fn in os.listdir('.'):
            if ((str(fn).find("profile") == 0) and
                    (str(fn).find(".txt") == (len(str(fn)) - 4))):
                self.__prof_list.append(str(fn))
            elif ((str(fn).find("dict_profile") == 0) and
                      (str(fn).find(".txt") == (len(str(fn)) - 4))):
                self.__dict_list.append(str(fn))
        self.__frames.append(tkinter.Frame(self.__gui))
        self.__frames.append(tkinter.Frame(self.__gui))

        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Filename",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="GUI header",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Text size",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # preview size
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Preview size",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # button height
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Button height",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # button width
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Button width",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # transparency index
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Transparency",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.Entry(self.__frames[0]))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1
        # flash color
        self.__flash = tkinter.StringVar(self.__frames[0])
        self.__flash.set("white")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Flash color",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__flash,
                                                 "white",
                                                 "yellow",
                                                 "black",
                                                 "orange",
                                                 "pink",
                                                 "green"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # caps color
        self.__caps = tkinter.StringVar(self.__frames[0])
        self.__caps.set("white")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Caps color",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__caps,
                                                 "white",
                                                 "yellow",
                                                 "black",
                                                 "orange",
                                                 "pink",
                                                 "green"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # map id text color
        self.__mapidText = tkinter.StringVar(self.__frames[0])
        self.__mapidText.set("white")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="MapID text color",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__mapidText,
                                                 "white",
                                                 "yellow",
                                                 "black",
                                                 "orange",
                                                 "pink",
                                                 "green"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # map id bg color
        self.__mapidBg = tkinter.StringVar(self.__frames[0])
        self.__mapidBg.set("white")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="MapID color",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__mapidBg,
                                                 "white",
                                                 "yellow",
                                                 "black",
                                                 "orange",
                                                 "pink",
                                                 "green"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # key bg color
        self.__keyBg = tkinter.StringVar(self.__frames[0])
        self.__keyBg.set("white")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Key color",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__keyBg,
                                                 "white",
                                                 "yellow",
                                                 "black",
                                                 "orange",
                                                 "pink",
                                                 "green"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # key text color
        self.__keyText = tkinter.StringVar(self.__frames[0])
        self.__keyText.set("white")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Key text color",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__keyText,
                                                 "white",
                                                 "yellow",
                                                 "black",
                                                 "orange",
                                                 "pink",
                                                 "green"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        # preview boolean flag
        self.__show = tkinter.StringVar(self.__frames[0])
        self.__show.set("Yes")
        self.__labels.append(tkinter.Label(self.__frames[0],
                                           text="Show labels?",
                                           font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              column=0, sticky="wens")
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__show,
                                                 "Yes",
                                                 "No"))
        self.__entries[self.__rowCounter].grid(row=self.__rowCounter,
                                               column=1, columnspan=2,
                                               sticky="wens")
        self.__rowCounter += 1

        self.__labels.append(
            tkinter.Label(self.__frames[0],
                          text="For each page, type 14 strings (with spaces " + '\n' +
                               "in between) that will correspond with the keys " + '\n' +
                               "* - + 7 8 9 4 5 6 1 2 3 0 .",
                          font=self.__textFont))
        self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                              columnspan=3, sticky="wens")

        self.__startPageIdx = self.__rowCounter
        self.__rowCounter += 1

        for x in range(0, 6):
            self.__entries.append(tkinter.Entry(self.__frames[0]))
            self.__labels.append(tkinter.Label(self.__frames[0],
                                               text="Page " + str(x),
                                               font=self.__textFont))
            self.__labels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__entries[self.__rowCounter - 1].grid(row=self.__rowCounter,
                                                       column=1, columnspan=2,
                                                       sticky="wens")
            self.__rowCounter += 1

        self.__switchFile = tkinter.StringVar(self.__frames[0])



        self.__switchFile.set(str(self.__currProf))
        self.__switchFile.trace("w", self.option_change)

        # self.__profileOptionMenu = self.__rowCounter
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__switchFile,
                                                 *self.__prof_list))
        self.__btns.append(tkinter.Button(self.__frames[0], text="Save",
                                          font=self.__textFont,
                                          command=lambda: self.error_check()))
        self.__btns.append(tkinter.Button(self.__frames[0], text="Switch",
                                          font=self.__textFont,
                                          command=lambda: self.fname_check()))
        self.__entries[self.__rowCounter - 1].grid(row=self.__rowCounter,
                                                   column=0, sticky="wens")
        self.__btns[0].grid(row=self.__rowCounter, column=1, sticky="wens")
        self.__btns[1].grid(row=self.__rowCounter, column=2, sticky="wens")
        # put in row 1 so errors will show up in row 0 for self.__frames[1]
        self.__frames[0].grid(row=1, sticky="wens")

        content = self.get_profile_content(self.__currProf)
        self.change_content(content)


    ## NEED TO CHECK IF THIS IS HANDLED PROPERLY
    def fname_check(self):
        with open("lastProfile.txt", "w") as write_switch:
            write_switch.write(str(self.__switchFile.get()))
        write_switch.close()
        self.__gui.destroy()

    def error_check(self):
        self.__frames[1].grid_forget()
        # the frame ideally should remove itself
        # from the grid before getting "deallocated"
        # to prevent having extra unused space in the grid
        self.__errors = []
        self.__errorLabels = []
        if str(self.__entries[0].get()) == "":
            self.__errors.append("Need a filename")
        if len(self.__entries[1].get()) > 20:
            self.__errors.append("Header too long")
        if len(self.__entries[1].get()) < 1:
            self.__errors.append("Header too short")
        try:
            ts = int(self.__entries[2].get())
            if (ts < 8):
                self.__errors.append("Text size too small")
        except ValueError:
            self.__errors.append("Text size not an int")
        try:
            ps = int(self.__entries[3].get())
            if (ps < 4):
                self.__errors.append("Preview size too small")
        except ValueError:
            self.__errors.append("Preview size not an int")
        try:
            bh = int(self.__entries[4].get())
            if (bh < 1):
                self.__errors.append("Button height too small")
        except ValueError:
            self.__errors.append("Button height not an int")
        try:
            bw = int(self.__entries[5].get())
            if (bw < 1):
                self.__errors.append("Button width too small")
        except ValueError:
            self.__errors.append("Button width not an int")
        try:
            ti = float(self.__entries[6].get())
            if (ti < 0):
                self.__errors.append("Transparency too small")
            elif (ti > 1):
                self.__errors.append("Transparency too large")
        except ValueError:
            self.__errors.append("Transparency not a float")

        for i in range(0, 6):
            if len(str(self.__entries[self.__startPageIdx + i].get()).split(' ')) > 14:
                self.__errors.append("Too many in page " + str(i))
            elif len(str(self.__entries[self.__startPageIdx + i].get()).split(' ')) < 14:
                self.__errors.append("Not enough in page " + str(i))
        if len(self.__errors) > 0:
            self.__frames.pop()
            self.__frames.append(tkinter.Frame(self.__gui))
            err_thread = threading.Thread(target=self.print_errors)
            err_thread.start()
        else:
            self.check_profile()

    def check_profile(self):
        for fn in os.listdir('.'):
            if (str(fn) == ("profile" + str(self.__entries[0].get()) + ".txt")):
                self.__warning = tkinter.Toplevel()
                self.__w_msg = tkinter.Label(self.__warning, text="Do you want to overwrite " +
                                                                  str(fn) + "?", font=self.__textFont)
                self.__w_msg.grid(row=0, columnspan=2, sticky="wens")
                self.__w_cancel = tkinter.Button(self.__warning, text="Cancel",
                                                 font=self.__textFont, command=lambda: self.dialog(False))
                self.__w_confirm = tkinter.Button(self.__warning, text="Confirm",
                                                  font=self.__textFont, command=lambda: self.dialog(True))
                self.__w_cancel.grid(row=4, column=0, sticky="wens")
                self.__w_confirm.grid(row=4, column=1, sticky="wens")

                self.__radioSelect = tkinter.IntVar()
                self.__radioSelect.set(0)
                self.__radioYes = tkinter.Radiobutton(self.__warning,
                                                      text="Clear dictionary",
                                                      font=self.__textFont,
                                                      variable=self.__radioSelect,
                                                      value=1).grid(row=1, columnspan=2, sticky="wens")
                self.__radioNo = tkinter.Radiobutton(self.__warning,
                                                     text="Keep dictionary",
                                                     font=self.__textFont,
                                                     variable=self.__radioSelect,
                                                     value=0).grid(row=2, columnspan=2, sticky="wens")
                self.__radioAdd = tkinter.Radiobutton(self.__warning,
                                                      text="Append dictionary",
                                                      font=self.__textFont,
                                                      variable=self.__radioSelect,
                                                      value=2).grid(row=3, column=0, sticky="wens")
                self.__addDict = tkinter.StringVar(self.__warning)
                self.__addDict.set(self.__dict_list[0])
                self.__dictlist = tkinter.OptionMenu(self.__warning,
                                                     self.__addDict,
                                                     *self.__dict_list).grid(row=3, column=1, sticky="wens")

                self.__warning.columnconfigure(0, weight=1)
                self.__warning.columnconfigure(1, weight=1)
                return
        # added a new profile to current directory
        self.__prof_list.append("profile" + str(self.__entries[0].get()) + ".txt")
        self.__entries[self.__rowCounter - 1].grid_forget()
        self.__entries.pop()
        self.__entries.append(tkinter.OptionMenu(self.__frames[0],
                                                 self.__switchFile,
                                                 *self.__prof_list))
        self.__entries[self.__rowCounter - 1].grid(row=self.__rowCounter, column=0,
                                                   sticky="wens")
        self.create_profile(0)

    def dialog(self, response):
        self.__warning.destroy()
        if response is True:
            self.create_profile(int(self.__radioSelect.get()))

    def create_profile(self, dictOptIdx):
        # dictOptIdx = 0 if keep dict, 1 if reset dict, 2 if add to dict
        fn_suffix = "profile" + str(self.__entries[0].get()) + ".txt"
        with open(fn_suffix, "w") as new_prof:
            # write the non-mapping data
            new_prof.write("dict_" + fn_suffix + '\n' +
                           str(self.__entries[1].get()) + '\n' +
                           str(self.__entries[2].get()) + " " +
                           str(self.__entries[3].get()) + " " +
                           str(self.__entries[4].get()) + " " +
                           str(self.__entries[5].get()) + " " +
                           str(self.__entries[6].get()) + " " +
                           str(self.__flash.get()) + " " +
                           str(self.__caps.get()) + " " +
                           str(self.__mapidText.get()) + " " +
                           str(self.__mapidBg.get()) + " " +
                           str(self.__keyBg.get()) + " " +
                           str(self.__keyText.get()) + " " +
                           str(self.__show.get()))
            # now write the mapping data
            for t in range(0, 6):
                new_prof.write('\n' + "Switch CapsLock " +
                               str(self.__entries[self.__startPageIdx + t].get()))
        new_prof.close()
        if(dictOptIdx is 1):
            with open("dict_" + fn_suffix, "w") as clear_dict:
                clear_dict.write("1 1 1")
            clear_dict.close()
        elif(dictOptIdx is 2):
            with open(self.__addDict.get(), "r") as read_otherdict:
                self.__extras = [line.rstrip('\n') for line in read_otherdict]
            read_otherdict.close()
            with open("dict_" + fn_suffix, "a") as append_dict:
                for i in range(1, len(self.__extras)):
                    append_dict.write('\n' + self.__extras[i])
            append_dict.close()


    def print_errors(self):
        for i in range(0, len(self.__errors)):
            self.__errorLabels.append(tkinter.Label(self.__frames[1],
                                                    text=self.__errors[i]))
            self.__errorLabels[i].grid(row=int(i / 3), column=(i % 3), sticky="wens")
        self.__frames[1].grid(row=0, sticky="wens")

    def option_change(self, *args):
        contents = self.get_profile_content(self.__switchFile.get())
        self.change_content(contents)

    def get_profile_content(self, file_name):
        # gets information from last used profile
        with open(file_name, "r") as curr_prof:
            content = [line.rstrip('\n') for line in curr_prof]
        curr_prof.close()
        return content

    def change_content(self,content):
        # profile name
        self.__entries[0].delete(0, len(self.__entries[0].get()))
        temp_file = self.__switchFile.get()
        show_file = temp_file[7:-4]
        self.__entries[0].insert(0,show_file)
        # GUI Header
        self.__entries[1].delete(0, len(self.__entries[1].get()))
        self.__entries[1].insert(0, str(content[1]))

        format = [item.rstrip(' ') for item in str(content[2]).split(' ')]

        #text size
        self.__entries[2].delete(0, len(self.__entries[2].get()))
        self.__entries[2].insert(0, str(format[0]))

        # preview size
        self.__entries[3].delete(0, len(self.__entries[3].get()))
        self.__entries[3].insert(0, str(format[1]))

        # Button height size
        self.__entries[4].delete(0, len(self.__entries[4].get()))
        self.__entries[4].insert(0, str(format[2]))

        # Button width size
        self.__entries[5].delete(0, len(self.__entries[5].get()))
        self.__entries[5].insert(0, str(format[3]))

        # Transparency
        self.__entries[6].delete(0, len(self.__entries[6].get()))
        self.__entries[6].insert(0, str(format[4]))

        # flash color
        self.__flash.set(str(format[5]))

        # caps color
        self.__caps.set(str(format[6]))

        # map id text color
        self.__mapidText.set(str(format[7]))

        # map id bg color
        self.__mapidBg.set(str(format[8]))

        # map Key bg folor
        self.__keyBg.set(str(format[9]))

        # map key text folor
        self.__keyText.set(str(format[10]))

        # set
        self.__show.set(str(format[11]))

        for i in range(0,6):
            remove_len = len("Switch CapsLock ")
            temp_string = content[3+i][remove_len:]
            self.__entries[14+i].delete(0, len(self.__entries[14+i].get()))
            self.__entries[14+i].insert(0, temp_string)

    def run(self):
        self.__gui.mainloop()
        print("done")


app = PROFILE_GUI()
app.run()
