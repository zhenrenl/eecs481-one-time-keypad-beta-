import datetime
import time
import tkinter
import tkinter.font as Tkfont
import os
import sys

from pykeyboard import PyKeyboard

# 'default' time spent between each user key input
SLEEP_TIME = 0.5

class LIST_GUI():
    def __init__(self):
        self.loadProfile(True)

    # switches from curr profile to nextFile profile
    def changeProfile(self, nextFile, readDict):
        self.closeProfile(nextFile)
        self.loadProfile(readDict)

    def loadProfile(self, readDict):
        # next_word is the word currently being typed by user
        self.__next_word = ""
        # rec is a list of recommended words
        self.__rec = []
        # num is a list of the word count of the recommended words
        self.__num = []
        # MAGIC_NUM is the number of recommended words
        self.__MAGIC_NUM = 4
        # the dictionary of words and corresponding word counts from user
        self.__dict = {}
        # number of words typed by user so far
        self.__num_words = 0
        # amount of time spent by user typing so far
        self.__old_time = 0.0
        # filename storing current profile
        self.__profile = ""
        # options on rec word buttons when next_word is empty string
        self.__options = ["ABOUT", "TUTORIAL", "PROFILES", "EXIT"]
        # fixed buttons
        self.__fixedBtns = ["Space", "Back", "Return"]
        # generated tab flag
        self.__hasTabbed = False
        # generated switch flag
        self.__hasSwitched = False
        # generated addPreviews flag
        self.__addPreviews = False
        # initialize the recommended words GUI
        self.__gui = tkinter.Tk()
        self.__mainframe = tkinter.Frame(self.__gui)
        self.__mainframe.grid(row=5, column=5)
        self.__defaultbg = self.__gui.cget('bg')
        self.__btns = []
        self.__btntexts = []
        self.__previews = []
        self.__frames = []
        self.__fonts = []
        # a list of a numLockEnabled list and a numLockDisabled list
        self.__keyTypes = ["Numlock", "Divide", "Multiply", "Subtract",
                           "Add", "Numpad7", "Home", "Numpad8", "Up",
                           "Numpad9", "Prior", "Numpad4", "Left", "Numpad5",
                           "Clear", "Numpad6", "Right", "Numpad1","End",
                           "Numpad2", "Down", "Numpad3", "Next", "Numpad0",
                           "Insert", "Decimal", "Delete"]
        #self.__custTypes = ["*", "-", "+", "7", "8", "9", "4", "5", "6", "1",
        #                    "2", "3", "0", "."]
        self.__SWITCH = 0
        self.__CAPS = 0
        self.__PAGES = []
        self.__hotkeys = ["Browser_Home", "Tab", "Launch_Mail", "Launch_App2"]
        # creates a frame for each column of buttons in GUI
        for idx in range(0, 7):
            self.__frames.append(tkinter.Frame(self.__mainframe))
        # gets filename of last used profile
        with open("lastProfile.txt", "r") as check_prof:
            ln = [line.rstrip('\n') for line in check_prof]
            self.__profile = str(ln[0])
        check_prof.close()
        # gets information from last used profile
        with open(self.__profile, "r") as curr_prof:
            content = [line.rstrip('\n') for line in curr_prof]
            # dict of  the profile
            self.__dictfile = str(content[0])
            # title of the profile
            self.__gui.title(str(content[1]))
            # set font for keypad
            self.__fonts.append(
                tkinter.font.Font(size=int(content[2].split(' ')[0])))
            # set font for mapped keys preview
            self.__fonts.append(
                tkinter.font.Font(size=int(content[2].split(' ')[1])))
            # set button height
            self.__btnHeight = int(content[2].split(' ')[2])
            # set button width
            self.__btnWidth = int(content[2].split(' ')[3])
            # set transparency index (high is opaque)
            self.__gui.attributes("-alpha", float(content[2].split(' ')[4]))
            # set flashOn color
            self.__flashbg = str(content[2].split(' ')[5])
            # set capsOn color
            self.__capsbg = str(content[2].split(' ')[6])
            # set switch map keys color
            self.__switchmapbg = str(content[2].split(' ')[7])
            # set mapping id color
            self.__mapidbg = str(content[2].split(' ')[8])
            # set key bg color
            self.__keybg = str(content[2].split(' ')[9])
            # set key text fg color
            self.__textfg = str(content[2].split(' ')[10])
            # boolean to show labels or not
            if(str(content[2].split(' ')[11]) == "Yes"):
                self.__addPreviews = True
            # add the 6 key mappings to PAGES
            for i in range(0, 6):
                tempDict = {}
                tempStr = ""
                tempMap = content[i + 3].split(' ')
                for q in range(0, 5):
                    tempDict[self.__keyTypes[q]] = tempMap[q]
                    tempStr += (" " + tempMap[q])
                    if ((q % 4) is 3):
                        tempStr += " "
                        self.__previews.append(tkinter.Button(
                            self.__frames[1], text=tempStr,
                            font=self.__fonts[1]))
                        tempStr = ""
                q = 5
                for r in range(5, len(tempMap)):
                    tempDict[self.__keyTypes[q]] = tempMap[r]
                    q += 1
                    tempDict[self.__keyTypes[q]] = tempMap[r]
                    q += 1
                    tempStr += (" " + tempMap[r])
                    if((r % 4) is 3):
                        tempStr += " "
                        self.__previews.append(tkinter.Button(
                            self.__frames[1], text=tempStr,
                            font=self.__fonts[1]))
                        tempStr = ""
                self.__PAGES.append(tempDict)
        curr_prof.close()
        with open(self.__dictfile, "r") as dict_read:
            content = [line.rstrip('\n') for line in dict_read]
            # store total number of words and total runtime of profile
            self.__num_words = int(content[0].split(' ')[0])
            self.__old_time = float(content[0].split(' ')[1])
            for j in range(1, len(content)):
                self.__dict[str(content[j].split(' ')[0])] = \
                    int(content[j].split(' ')[1])
        dict_read.close()
        # initialize NumLock button
        self.__btns.append(tkinter.Button(
            self.__frames[2],
            text=self.__PAGES[0][self.__keyTypes[0]],
            bg=self.__keybg,
            fg=self.__textfg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            font=self.__fonts[0]))
        self.__btntexts.append(
            self.__PAGES[0][self.__keyTypes[0]])
        # initialize / button
        self.__btns.append(tkinter.Button(
            self.__frames[3],
            text=self.__PAGES[0][self.__keyTypes[1]],
            bg=self.__keybg,
            fg=self.__textfg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            font=self.__fonts[0]))
        self.__btntexts.append(
            self.__PAGES[0][self.__keyTypes[1]])
        # initialize * button
        self.__btns.append(tkinter.Button(
            self.__frames[4],
            text=self.__PAGES[0][self.__keyTypes[2]],
            bg=self.__keybg,
            fg=self.__textfg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            font=self.__fonts[0]))
        self.__btntexts.append(
            self.__PAGES[0][self.__keyTypes[2]])
        # initialize - button
        self.__btns.append(tkinter.Button(
            self.__frames[5],
            text=self.__PAGES[0][self.__keyTypes[3]],
            bg=self.__keybg,
            fg=self.__textfg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            font=self.__fonts[0]))
        self.__btntexts.append(
            self.__PAGES[0][self.__keyTypes[3]])
        # initialize + button
        self.__btns.append(tkinter.Button(
            self.__frames[5],
            text=self.__PAGES[0][self.__keyTypes[4]],
            bg=self.__keybg,
            fg=self.__textfg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            font=self.__fonts[0]))
        self.__btntexts.append(
            self.__PAGES[0][self.__keyTypes[4]])
        # initialize 0 - 9 buttons
        q = 5
        for i in range(0, 10):
            self.__btns.append(tkinter.Button(
                self.__frames[(i % 3) + 2],
                text=self.__PAGES[0][self.__keyTypes[q]],
                bg=self.__keybg,
                height=self.__btnHeight,
                width=self.__btnWidth,
                fg=self.__textfg,
                font=self.__fonts[0]))
            self.__btntexts.append(
                self.__PAGES[0][self.__keyTypes[q]])
            q += 2
        # initialize . button
        self.__btns.append(tkinter.Button(
            self.__frames[4],
            text=self.__PAGES[0][self.__keyTypes[q]],
            bg=self.__keybg,
            width=self.__btnWidth,
            fg=self.__textfg,
            height=self.__btnHeight,
            font=self.__fonts[0]))
        self.__btntexts.append(
            self.__PAGES[self.__SWITCH][self.__keyTypes[q]])
        # the space button
        self.__btns.append(tkinter.Button(
            self.__frames[3], text="Space",
            bg=self.__keybg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            fg=self.__textfg,
            font=self.__fonts[0]))
        self.__btntexts.append("Space")
        # the back button
        self.__btns.append(tkinter.Button(
            self.__frames[5], text="Back",
            bg=self.__keybg,
            fg=self.__textfg,
            width=self.__btnWidth,
            height=self.__btnHeight,
            font=self.__fonts[0]))
        self.__btntexts.append("Back")
        # the enter button
        self.__btns.append(tkinter.Button(
            self.__frames[5], text="Enter",
            bg=self.__keybg,
            fg=self.__textfg,
            width=self.__btnWidth,
            height=self.__btnHeight,
            font=self.__fonts[0]))
        self.__btntexts.append("Return")
        # packing the 'column 2' buttons
        self.packButtons([0, 5, 8, 11, 14], 2)
        # packing the 'column 3' buttons
        self.packButtons([1, 6, 9, 12, 16], 3)
        # packing the 'column 4' buttons
        self.packButtons([2, 7, 10, 13, 15], 4)
        # packing the 'column 5' buttons
        self.packButtons([17, 3, 4, 18], 5)
        # packing the 'column 6' buttons (i.e. rec list)
        idx = 0
        while idx < self.__MAGIC_NUM:
            # initialize recommended words to empty string
            self.__rec.append("")
            self.__num.append(0)
            self.__btns.append(
                tkinter.Button(self.__frames[6],
                               text=self.__options[idx],
                               font=self.__fonts[0]))
            self.__btntexts.append(self.__options[idx])
            self.__btns[idx + 19].grid(row=idx, sticky="wens")
            self.__frames[6].rowconfigure(idx, weight=1)
            idx += 1
        # packing the 'column 0' buttons (i.e. map numbers)
        for v in range(0, 6):
            mapNumBg = self.__defaultbg
            if v is 0:
                mapNumBg = self.__mapidbg
            self.__btns.append(
                tkinter.Button(self.__frames[0],
                               text=str(v),
                               font=self.__fonts[0],
                               bg=mapNumBg))
            self.__btntexts.append(str(v))
            self.__btns[v + 19 + self.__MAGIC_NUM].grid(row=v,
                                                        sticky="wens")
            self.__frames[0].rowconfigure(v, weight=1)
        # create wpm statistic button
        self.__btns.append(
            tkinter.Button(self.__frames[6], text=str(self.__num_words / self.__old_time)))
        self.__btns[19 + self.__MAGIC_NUM + 6].grid(row=4, sticky="wens")
        # add wpm btn to last row of column 6
        self.__frames[6].rowconfigure(4)
        # set up column 1 as preview of mapping's contents if addPreview flag is True
        if self.__addPreviews is True:
            for j in range(0, len(self.__previews)):
                self.__previews[j].grid(row=j, sticky="wens")
                self.__frames[1].rowconfigure(j, weight=1)
        # adds each column frame to the GUI
        for k in range(0, len(self.__frames)):
            self.__frames[k].grid(row=0, column=k, sticky="wens")
        # saves starting time of current profile run
        self.__start_time = datetime.datetime.now().time()

    def closeProfile(self, nextProfile):
        add_time = self.diffTime(self.__start_time, datetime.datetime.now().time())
        # Stores the cumulative runtime of the application over all user sessions
        new_time = self.__old_time + add_time
        with open(self.__dictfile, "w") as close_profdict:
            # Update num_words, cumulative runtime, and words-per-minute in profile
            close_profdict.write(str(self.__num_words) + " " +
                             str(new_time) + " " +
                             str(self.__num_words / new_time))
            # Stores word count of each word from dictionary in profile
            for word in self.__dict:
                close_profdict.write('\n' + str(word) + " " +
                                 str(self.__dict[word]))
        close_profdict.close()
        # Saves the filename of current profile
        with open("lastProfile.txt", "r+") as save_prof:
            save_prof.seek(0)
            save_prof.write(nextProfile)
        save_prof.close()

    # Called when user finishes typing or selecting a word
    def updateDict(self, event):
        print("Added: " + event)
        # number of user's typed words gets incremented by 1
        self.__num_words += 1
        # update the word count of the typed word
        if event in self.__dict:
            self.__dict[event] += 1
        else:
            self.__dict[event] = 1
        # clear next_word back to the empty string
        self.__next_word = ""
        # update wpm
        temp_time = self.__old_time + self.diffTime(self.__start_time, datetime.datetime.now().time())
        self.__btns[19 + self.__MAGIC_NUM + 6].config(text=str(self.__num_words / temp_time))
        # reset the recommendation word list to show options
        self.clearList()
        self.updateList(True)

    # rewrite keypad
    def changeKeypad(self, switchDone):
        if switchDone:
            # changing 2nd btn back to CapsLock with proper color
            capsBg = self.__keybg
            if self.__CAPS is 1:
                capsBg = self.__capsbg
            self.__btns[1].config(
                text=self.__PAGES[self.__SWITCH]
                [self.__keyTypes[1]], bg=capsBg)
            self.__btntexts[1] = self.__PAGES[
                self.__SWITCH][self.__keyTypes[1]]
            # changing the next 3 buttons to new mapping's symbols
            for i in range(2, 5):
                self.__btns[i].config(
                    text=self.__PAGES[self.__SWITCH]
                    [self.__keyTypes[i]], bg=self.__keybg)
                self.__btntexts[i] = self.__PAGES[
                    self.__SWITCH][self.__keyTypes[i]]
            q = 5
            # changing the remaining customizable buttons
            for j in range(5, 16):
                self.__btns[j].config(
                    text=self.__PAGES[self.__SWITCH]
                    [self.__keyTypes[q]], bg=self.__keybg)
                self.__btntexts[j] = self.__PAGES[
                    self.__SWITCH][self.__keyTypes[q]]
                q += 2
            # changing 18th button back to Back
            self.__btns[17].config(text="Back", bg=self.__keybg)
            self.__btntexts[17] = "Back"
        else:
            self.__btns[1].config(text="0", bg=self.__switchmapbg)
            self.__btntexts[1] = "0"
            self.__btns[2].config(text="1", bg=self.__switchmapbg)
            self.__btntexts[2] = "1"
            self.__btns[17].config(text="2", bg=self.__switchmapbg)
            self.__btntexts[17] = "2"
            self.__btns[6].config(text="3", bg=self.__switchmapbg)
            self.__btntexts[6] = "3"
            self.__btns[7].config(text="4", bg=self.__switchmapbg)
            self.__btntexts[7] = "4"
            self.__btns[3].config(text="5", bg=self.__switchmapbg)
            self.__btntexts[3] = "5"

    # packs the buttons from num_list in the col_num frame
    def packButtons(self, num_list, col_num):
        idx = 0
        for num in num_list:
            self.__btns[int(num)].grid(row=idx, sticky="wens")
            self.__frames[col_num].rowconfigure(idx, weight=1)
            idx += 1
        # configuring the column with 'Enter' button
        if len(num_list) is not 5:
            self.__frames[col_num].rowconfigure(0, weight=0)
            self.__frames[col_num].rowconfigure(1, weight=0)
            self.__frames[col_num].rowconfigure(2, weight=0)
            self.__frames[col_num].rowconfigure(3, weight=1)

    # Removes all recommended words
    def clearList(self):
        idx = 0
        while idx < self.__MAGIC_NUM:
            self.__rec[idx] = ""
            self.__num[idx] = 0
            idx += 1

    # Display each current recommended word or option on the GUI
    def updateList(self, nextWordEmpty):
        idx = 0
        while idx < self.__MAGIC_NUM:
            if nextWordEmpty is True:
                self.__btns[idx + 19].config(text=self.__options[idx])
                self.__btntexts[idx + 19] = self.__options[idx]
            else:
                self.__btns[idx + 19].config(text=self.__rec[idx])
                self.__btntexts[idx + 19] = self.__rec[idx]
            #self.__btns[idx + 19].config(bg=self.__defaultbg)
            idx += 1

    # Calculates the difference in time between old and new (in minutes)
    def diffTime(self, old, new):
        sec = int(new.second) - int(old.second)
        if(sec < 0):
            sec += 60
        min = int(new.minute) - int(old.minute)
        if(min < 0):
            min += 60
        hr = int(new.hour) - int(old.hour)
        if(hr < 0):
            hr += 24
        return (sec / 60) + min + (60 * hr)

    # Starts the main GUI application
    def run(self):
        # Runs 'infinite' loop awaiting user input
        self.__gui.mainloop()
        # saves profile before exit and will load it next time
        self.closeProfile(self.__profile)

    # Checks if word contains the user's currently typed word
    def findWord(self, word, small_word):
        if word.find(small_word) == 0:
            return True
        else:
            return False

    def caps(self, msg):
        if self.__CAPS is 1 and msg.isalpha() and len(msg) is 1:
            return msg.upper()
        else:
            return msg

    def flash(self, idx, flag):
        if idx is 1 and self.__CAPS is 1 and flag is True:
            self.__btns[1].configure(bg=self.__capsbg)
        elif idx is 1 and self.__CAPS is 0 and flag is True:
            self.__btns[1].configure(bg=self.__keybg)
        elif flag is True and idx is not 1:
            self.__btns[idx].configure(bg=self.__flashbg)
        elif idx is not 1 and idx in range(0, 19):
            self.__btns[idx].configure(bg=self.__keybg)
        elif idx is not 1:
            self.__btns[idx].configure(bg=self.__defaultbg)

    # creates another window corresponding to selected option
    # NOT COMPLETED.....
    def systemCall(self, optionIdx):
        if optionIdx is 0:
            about = tkinter.Toplevel(self.__gui)
            about_course = tkinter.Label(about, text="EECS 481 SECTION 002",
                                        font=self.__fonts[0])
            about_group = tkinter.Label(about, text="ONE-TIME KEYPAD (2017)",
                                        font=self.__fonts[0])
            about_contact = tkinter.Label(about, text="CONTACT INFORMATION",
                                          font=self.__fonts[0])
            about_mem1 = tkinter.Label(about,
                                       text="Zhenren Lu: zhenrenl@umich.edu",
                                       font=self.__fonts[0])
            about_mem2 = tkinter.Label(about,
                                       text="Surab Shrestha: sbshrest@umich.edu",
                                       font=self.__fonts[0])
            about_mem3 = tkinter.Label(about,
                                       text="Arjun Saxena: arjunsax@umich.edu",
                                       font=self.__fonts[0])
            about_mem4 = tkinter.Label(about,
                                       text="Parth Joshi: pgjoshi@umich.edu",
                                       font=self.__fonts[0])
            about_course.grid(row=0, sticky="wens")
            about_group.grid(row=1, sticky="wens")
            about_contact.grid(row=2, sticky="wens")
            about_mem1.grid(row=3, sticky="wens")
            about_mem2.grid(row=4, sticky="wens")
            about_mem3.grid(row=5, sticky="wens")
            about_mem4.grid(row=6, sticky="wens")
        elif optionIdx is 1:
            tutorial = tkinter.Toplevel(self.__gui)
            tutorial_title = tkinter.Label(tutorial, text="TUTORIAL",
                                           font=self.__fonts[0])
            tutorial_title.grid(row=0, sticky="wens")
        elif optionIdx is 2:
            os.system("profile.py")
            temp_profile = ""
            with open("lastProfile.txt", "r") as read_lp:
                temp_profile += read_lp.readline()
            read_lp.close()
            if(temp_profile != self.__profile):
                self.changeProfile(temp_profile, True)
            else:
                self.changeProfile(temp_profile, False)
        elif optionIdx is 3:
            sys.exit()


    def changeMapId(self, nextSwitchID):
        self.__btns[19 + self.__MAGIC_NUM +
                    self.__SWITCH].config(bg=self.__defaultbg)
        self.__SWITCH = nextSwitchID
        self.__btns[19 + self.__MAGIC_NUM +
                    self.__SWITCH].config(bg=self.__mapidbg)

    def keyDown(self, event):
        k = PyKeyboard()
        msg = str(event.Key)
        # user clicked one of the 16 customizable keys while not switching
        if event.Key in self.__keyTypes and not self.__hasSwitched:
            msg = self.__PAGES[self.__SWITCH][event.Key]
            idx = self.__btntexts.index(msg)
            # Switch to next mapping
            if msg == "Switch":
                self.__hasSwitched = True
                self.changeMapId((self.__SWITCH + 1) % len(self.__PAGES))
                self.changeKeypad(False)
            # Clear or set the CapsLock flag
            elif msg == "CapsLock":
                self.__CAPS = (self.__CAPS + 1) % 2
            # Print a tab on the screen
            elif msg == "Tab":
                self.__hasTabbed = True
                k.type_string('\t')
            # Print the mapped symbol on screen
            else:
                msg = self.caps(msg)
                k.type_string(msg)
            self.flash(idx, True)
            self.auto_complete(msg)
            del k
            return False
        # user clicked one of the 4 top hotkeys while not switching
        elif event.Key in self.__hotkeys and not self.__hasTabbed \
            and not self.__hasSwitched:
            idx = self.__hotkeys.index(event.Key)
            recWord = self.__rec[idx]
            if(len(recWord) > 0):
                self.flash(idx + 19, True)
                if(self.__next_word != recWord):
                    k.type_string(recWord[len(self.__next_word): len(recWord)])
                self.updateDict(recWord)
            elif(len(self.__next_word) is 0):
                self.flash(idx + 19, True)
                #self.systemCall(idx)
            del k
            return False
        # user clicked another key while switching
        elif(event.Key in self.__hotkeys and not self.__hasTabbed) \
            or (event.Key in self.__fixedBtns and self.__hasSwitched) \
            or (event.Key in self.__keyTypes):
            if msg == "Divide":
                self.__btns[1].configure(bg=self.__flashbg)
            elif msg == "Multiply":
                self.__btns[2].configure(bg=self.__flashbg)
            elif msg == "Back":
                self.__btns[17].configure(bg=self.__flashbg)
            elif msg == "Numpad8" or msg == "Up":
                self.__btns[6].configure(bg=self.__flashbg)
            elif msg == "Numpad9" or msg == "Prior":
                self.__btns[7].configure(bg=self.__flashbg)
            elif msg == "Subtract":
                self.__btns[3].configure(bg=self.__flashbg)
            del k
            return False
        # user clicked "Space", "Back", or "Enter" while not switching
        elif event.Key in self.__fixedBtns:
            idx = self.__fixedBtns.index(event.Key)
            self.flash(idx + 16, True)
            self.auto_complete(msg)
        # ignores program-generated tab
        elif event.Key in self.__hotkeys:
            self.__hasTabbed = False
        del k
        return True

    def keyUp(self, event):
        k = PyKeyboard()
        msg = str(event.Key)
        if msg == "Numlock":
            self.__hasSwitched = False
            self.changeKeypad(True)
            self.flash(0, False)
            del k
            return False
        elif self.__hasSwitched:
            if msg == "Divide":
                self.changeMapId(0)
                self.__btns[1].configure(bg=self.__switchmapbg)
            elif msg == "Multiply":
                self.changeMapId(1)
                self.__btns[2].configure(bg=self.__switchmapbg)
            elif msg == "Back":
                self.changeMapId(2)
                self.__btns[17].configure(bg=self.__switchmapbg)
            elif msg == "Numpad8" or msg == "Up":
                self.changeMapId(3)
                self.__btns[6].configure(bg=self.__switchmapbg)
            elif msg == "Numpad9" or msg == "Prior":
                self.changeMapId(4)
                self.__btns[7].configure(bg=self.__switchmapbg)
            elif msg == "Subtract":
                self.changeMapId(5)
                self.__btns[3].configure(bg=self.__switchmapbg)
            del k
            return False
        elif event.Key in self.__keyTypes:
            msg = self.__PAGES[self.__SWITCH][event.Key]
            idx = self.__btntexts.index(msg)
            self.flash(idx, False)
            del k
            return False
        elif event.Key in self.__hotkeys:
            idx = self.__hotkeys.index(event.Key)
            self.flash(idx + 19, False)
            self.systemCall(idx)
            del k
            return False
        elif event.Key in self.__fixedBtns:
            idx = self.__fixedBtns.index(event.Key)
            self.flash(idx + 16, False)
        del k
        return True

    def searchDict(self):
        # Clear list to get fresh list of recommended words for next_word
        self.clearList()
        # Search dictionary for every word that contains next_word
        for word in self.__dict:
            if self.findWord(word, self.__next_word):
                idx = 0
                updated = False
                seen = False
                while not updated and (idx < self.__MAGIC_NUM) and not seen:
                    # word is already in recommended list, SKIP
                    if self.__rec[idx] is word:
                        seen = True
                    # word has better word count
                    elif self.__dict[word] > self.__num[idx]:
                        idx2 = self.__MAGIC_NUM - 1
                        while (idx2 > idx):
                            # Shifts recommended words down 1 ranking
                            self.__num[idx2] = self.__num[idx2 - 1]
                            self.__rec[idx2] = self.__rec[idx2 - 1]
                            idx2 -= 1
                        # Stores word at correct index of list
                        self.__num[idx2] = self.__dict[word]
                        self.__rec[idx2] = word
                        updated = True
                    # To compare with lower ranked recommendation word
                    idx += 1
        self.updateList(False)

    def auto_complete(self, event):
        # shorten currently typed word by 1 char if not the empty string
        if str(event) == "Back" and len(self.__next_word) > 0:
            self.__next_word = self.__next_word[0: len(self.__next_word) - 1]
        elif str(event).isalnum() and len(str(event)) is 1:
            self.__next_word += str(event)
            self.searchDict()
        # update word count of user's currently typed word
        elif len(self.__next_word) > 0 and \
            str(event) != "CapsLock" and str(event) != "Switch":
            self.updateDict(self.__next_word)

    def testAutoCom(self, *args):
        for file in args:
            # open each file and read it to simulate user input
            with open(str(file), "r") as open_input:
                lines = [line.rstrip('\n') for line in open_input]
                words = lines[0].split(' ')
                for word in words:
                    time.sleep(SLEEP_TIME)
                    # tests 'user input' on rec word list GUI system
                    self.auto_complete(str(word))
            open_input.close()


#if __name__ == "__main__":
#    app = LIST_GUI()
#    test = threading.Thread(target=app.testAutoCom,
#                            args=["sample_input1.txt",
#                                  "sample_input2.txt",
#                                  "sample_input3.txt"])
#    test.start()
#    app.run()
