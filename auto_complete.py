import datetime
import threading
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
        # initialize the recommended words GUI
        self.__gui = tkinter.Tk()
        self.__gui.resizable(width=False, height=False)
        self.loadProfile()

    # switches from curr profile to nextFile profile
    def changeProfile(self, nextFile):
        self.closeProfile(nextFile)
        self.loadProfile()

    def loadProfile(self):
        # next_word is the word currently being typed by user
        self.__next_word = ""
        # rec is a list of recommended words
        self.__rec = []
        # num is a list of the word count of the recommended words
        self.__num = []
        # MAGIC_NUM is the number of recommended words
        self.__MAGIC_NUM = 4
        # filename storing current profile
        self.__profile = ""
        # options on rec word buttons when next_word is empty string
        self.__options = ["ABOUT", "TUTORIAL", "PROFILES", "EXIT"]
        # fixed buttons
        self.__fixedBtns = ["Space", "Back", "Return"]
        # the dictionary of words and corresponding word counts from user
        self.__dict = {}
        # number of words typed by user so far
        self.__num_words = 0
        # amount of time spent by user typing so far
        self.__old_time = 0.0
        # generated hasAutoTyped flag
        self.__hasAutoTyped = False
        # generated tab flag
        self.__hasTabbed = False
        # generated switch flag
        self.__hasSwitched = False
        # generated addPreviews flag
        self.__addPreviews = False
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
                temp_word = str(content[j].split(' ')[0])
                temp_count = int(content[j].split(' ')[1])
                if temp_word in self.__dict:
                    print("already here")
                    self.__dict[temp_word] += temp_count
                else:
                    self.__dict[temp_word] = temp_count
        dict_read.close()
        # initialize NumLock button
        self.__btns.append(tkinter.Button(
            self.__frames[2],
            text=self.__PAGES[0][self.__keyTypes[0]],
            bg=self.__keybg,
            fg=self.__textfg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[0]])))))
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
            font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[1]])))))
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
            font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[2]])))))
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
            font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[3]])))))
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
            font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[4]])))))
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
                font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[q]])))))
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
            font=tkinter.font.Font(
                size=self.config_font(
                len(self.__PAGES[0][self.__keyTypes[q]])))))
        self.__btntexts.append(
            self.__PAGES[self.__SWITCH][self.__keyTypes[q]])
        # the space button
        self.__btns.append(tkinter.Button(
            self.__frames[3], text="Space",
            bg=self.__keybg,
            height=self.__btnHeight,
            width=self.__btnWidth,
            fg=self.__textfg,
            font=tkinter.font.Font(
                size=self.config_font(len("Space")))))
        self.__btntexts.append("Space")
        # the back button
        self.__btns.append(tkinter.Button(
            self.__frames[5], text="Back",
            bg=self.__keybg,
            fg=self.__textfg,
            width=self.__btnWidth,
            height=self.__btnHeight,
            font=tkinter.font.Font(
                size=self.config_font(len("Back")))))
        self.__btntexts.append("Back")
        # the enter button
        self.__btns.append(tkinter.Button(
            self.__frames[5], text="Enter",
            bg=self.__keybg,
            fg=self.__textfg,
            width=self.__btnWidth,
            height=self.__btnHeight,
            font=tkinter.font.Font(
                size=self.config_font(len("Enter")))))
        self.__btntexts.append("Return")
        # packing the 'column 6' buttons (i.e. rec list)
        idx = 0
        while idx < self.__MAGIC_NUM:
            # initialize recommended words to empty string
            self.__rec.append("")
            self.__num.append(0)
            self.__btns.append(
                tkinter.Button(self.__frames[2 + idx],
                               height=self.__btnHeight,
                               width=self.__btnWidth,
                               fg=self.__textfg,
                               bg=self.__keybg,
                               text=self.__options[idx],
                               font=tkinter.font.Font(
                size=self.config_font(len(self.__options[idx])))))
            self.__btntexts.append(self.__options[idx])
            self.__btns[idx + 19].grid(row=0, sticky="wens")
            #self.__frames[6].rowconfigure(idx, weight=1)
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
        #self.__btns.append(
        #    tkinter.Button(self.__frames[1], text=str(self.__num_words / self.__old_time)))
        #self.__btns[19 + self.__MAGIC_NUM + 6].grid(row=4, sticky="wens")
        # add wpm btn to last row of column 6
        #self.__frames[6].rowconfigure(4)
        # set up column 1 as preview of mapping's contents if addPreview flag is True
        # packing the 'column 2' buttons
        self.packButtons([19, 0, 5, 8, 11, 14], 2)
        # packing the 'column 3' buttons
        self.packButtons([20, 1, 6, 9, 12, 16], 3)
        # packing the 'column 4' buttons
        self.packButtons([21, 2, 7, 10, 13, 15], 4)
        # packing the 'column 5' buttons
        self.packButtons([22, 17, 3, 4, 18], 5)
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
        for idx in range(0, 7):
            self.__frames[idx].grid_forget()

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
        #temp_time = self.__old_time + self.diffTime(self.__start_time, datetime.datetime.now().time())
        #self.__btns[19 + self.__MAGIC_NUM + 6].config(text=str(self.__num_words / temp_time))
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
        if len(num_list) is not 6:
            self.__frames[col_num].rowconfigure(0, weight=0)
            self.__frames[col_num].rowconfigure(1, weight=0)
            self.__frames[col_num].rowconfigure(2, weight=0)
            self.__frames[col_num].rowconfigure(3, weight=0)
            self.__frames[col_num].rowconfigure(4, weight=1)

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
                self.__btns[idx + 19].config(text=self.__options[idx],
                        font=tkinter.font.Font(
                        size=self.config_font(len(self.__options[idx]))))
                self.__btntexts[idx + 19] = self.__options[idx]
            else:
                self.__btns[idx + 19].config(text=self.__rec[idx],
                        font=tkinter.font.Font(
                            size=self.config_font(len(self.__options[idx]))))
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
        elif idx is not 1:
            self.__btns[idx].configure(bg=self.__keybg)
        #elif idx is not 1 and idx in range(0, 19):
         #   self.__btns[idx].configure(bg=self.__keybg)

    # TUTORIAL NOT COMPLETED.....
    def systemCall(self, optionIdx):
        if optionIdx is 0:
            info = threading.Thread(target=self.about_us)
            info.start()
            info.join()
        elif optionIdx is 1:
            tut = threading.Thread(target=self.tutorial)
            tut.start()
            tut.join()
        elif optionIdx is 2:
            profiling = threading.Thread(target=self.profile_manager)
            profiling.start()
            profiling.join()
        elif optionIdx is 3:
            sys.exit()

    def config_font(self, length):
        return (self.__btnHeight * self.__btnWidth - length)

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
                self.__hasAutoTyped = True
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
            if(self.__hasAutoTyped):
                self.__hasAutoTyped = False
            else:
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
            if(len(self.__next_word) is 0):
                self.updateList(True)
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

    def about_us(self):
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

    def tutorial(self):
        tut = tkinter.Toplevel(self.__gui)
        tut_labels = []
        with open("USERGUIDE.txt", "r") as read_guide:
            contents = [line.rstrip('\n') for line in read_guide]
            for i in range(0, len(contents)):
                tut_labels.append(tkinter.Label(tut, text=contents[i],
                                                font=self.__fonts[0]))
                tut_labels[i].grid(row=i, sticky="wens")
        read_guide.close()


    def profile_manager(self):
            self.__profman = tkinter.Toplevel(self.__gui)
            self.__pmlabels = []
            self.__pmerrors = []
            self.__pmentries = []
            self.__pmerrorLabels = []
            # init list of profiles
            self.__prof_list = []
            self.__dict_list = []
            self.__pmframes = []
            self.__pmbtns = []
            self.__pmcurrProf = ""
            self.__pmtextFont = tkinter.font.Font(size=14)
            self.__pmerrFont = tkinter.font.Font(size=12)
            self.__rowCounter = 0
            self.__startPageIdx = 0

            # get current profile from lastProfile.txt
            with open("lastProfile.txt", "r") as read_lp:
                self.__pmcurrProf = read_lp.readline()

            # generate list of profiles
            for fn in os.listdir('.'):
                if ((str(fn).find("profile") == 0) and
                        (str(fn).find(".txt") == (len(str(fn)) - 4))):
                    self.__prof_list.append(str(fn))
                elif ((str(fn).find("dict_profile") == 0) and
                          (str(fn).find(".txt") == (len(str(fn)) - 4))):
                    self.__dict_list.append(str(fn))

            self.__pmframes.append(tkinter.Frame(self.__profman))
            self.__pmframes.append(tkinter.Frame(self.__profman))

            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Filename",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="GUI header",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Text size",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # preview size
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Preview size",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # button height
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Button height",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # button width
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Button width",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # transparency index
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Transparency",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1
            # flash color
            self.__pmflash = tkinter.StringVar(self.__pmframes[0])
            self.__pmflash.set("white")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Flash color",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmflash,
                                                     "white",
                                                     "yellow",
                                                     "black",
                                                     "orange",
                                                     "pink",
                                                     "green"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # caps color
            self.__pmcaps = tkinter.StringVar(self.__pmframes[0])
            self.__pmcaps.set("white")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Caps color",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmcaps,
                                                     "white",
                                                     "yellow",
                                                     "black",
                                                     "orange",
                                                     "pink",
                                                     "green"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # map id text color
            self.__pmmapidText = tkinter.StringVar(self.__pmframes[0])
            self.__pmmapidText.set("white")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="MapID text color",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmmapidText,
                                                     "white",
                                                     "yellow",
                                                     "black",
                                                     "orange",
                                                     "pink",
                                                     "green"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # map id bg color
            self.__pmmapidBg = tkinter.StringVar(self.__pmframes[0])
            self.__pmmapidBg.set("white")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="MapID color",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmmapidBg,
                                                     "white",
                                                     "yellow",
                                                     "black",
                                                     "orange",
                                                     "pink",
                                                     "green"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # key bg color
            self.__pmkeyBg = tkinter.StringVar(self.__pmframes[0])
            self.__pmkeyBg.set("white")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Key color",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmkeyBg,
                                                     "white",
                                                     "yellow",
                                                     "black",
                                                     "orange",
                                                     "pink",
                                                     "green"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # key text color
            self.__pmkeyText = tkinter.StringVar(self.__pmframes[0])
            self.__pmkeyText.set("white")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Key text color",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmkeyText,
                                                     "white",
                                                     "yellow",
                                                     "black",
                                                     "orange",
                                                     "pink",
                                                     "green"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            # preview boolean flag
            self.__pmshow = tkinter.StringVar(self.__pmframes[0])
            self.__pmshow.set("Yes")
            self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                               text="Show labels?",
                                               font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  column=0, sticky="wens")
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmshow,
                                                     "Yes",
                                                     "No"))
            self.__pmentries[self.__rowCounter].grid(row=self.__rowCounter,
                                                   column=1, columnspan=2,
                                                   sticky="wens")
            self.__rowCounter += 1

            self.__pmlabels.append(
                tkinter.Label(self.__pmframes[0],
                              text="For each page, type 14 strings (with spaces " + '\n' +
                                   "in between) that will correspond with the keys " + '\n' +
                                   "* - + 7 8 9 4 5 6 1 2 3 0 .",
                              font=self.__pmtextFont))
            self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                  columnspan=3, sticky="wens")

            self.__startPageIdx = self.__rowCounter
            self.__rowCounter += 1

            for x in range(0, 6):
                self.__pmentries.append(tkinter.Entry(self.__pmframes[0]))
                self.__pmlabels.append(tkinter.Label(self.__pmframes[0],
                                                   text="Page " + str(x),
                                                   font=self.__pmtextFont))
                self.__pmlabels[self.__rowCounter].grid(row=self.__rowCounter,
                                                      column=0, sticky="wens")
                self.__pmentries[self.__rowCounter - 1].grid(row=self.__rowCounter,
                                                           column=1, columnspan=2,
                                                           sticky="wens")
                self.__rowCounter += 1

            self.__pmswitchFile = tkinter.StringVar(self.__pmframes[0])

            self.__pmswitchFile.set(str(self.__pmcurrProf))
            self.__pmswitchFile.trace("w", self.option_change)

            # self.__profileOptionMenu = self.__rowCounter
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmswitchFile,
                                                     *self.__prof_list))
            self.__pmbtns.append(tkinter.Button(self.__pmframes[0], text="Save",
                                              font=self.__pmtextFont,
                                              command=lambda: self.error_check()))
            self.__pmbtns.append(tkinter.Button(self.__pmframes[0], text="Switch",
                                              font=self.__pmtextFont,
                                              command=lambda: self.perform_switch()))
            self.__pmentries[self.__rowCounter - 1].grid(row=self.__rowCounter,
                                                       column=0, sticky="wens")
            self.__pmbtns[0].grid(row=self.__rowCounter, column=1, sticky="wens")
            self.__pmbtns[1].grid(row=self.__rowCounter, column=2, sticky="wens")
            # put in row 1 so errors will show up in row 0 for self.__frames[1]
            self.__pmframes[0].grid(row=1, sticky="wens")

            content = self.get_profile_content(self.__pmcurrProf)
            self.change_content(content)

    def perform_switch(self):
        #with open("lastProfile.txt", "w") as write_switch:
        #    write_switch.write(str(self.__switchFile.get()))
        #write_switch.close()
        self.__profman.destroy()
        self.changeProfile(str(self.__pmswitchFile.get()))


    def error_check(self):
            self.__pmframes[1].grid_forget()
            # the frame ideally should remove itself
            # from the grid before getting "deallocated"
            # to prevent having extra unused space in the grid
            self.__pmerrors = []
            self.__pmerrorLabels = []
            if str(self.__pmentries[0].get()) == "":
                self.__pmerrors.append("Need a filename")
            if len(self.__pmentries[1].get()) > 20:
                self.__pmerrors.append("Header too long")
            if len(self.__pmentries[1].get()) < 1:
                self.__pmerrors.append("Header too short")
            try:
                ts = int(self.__pmentries[2].get())
                if (ts < 8):
                    self.__pmerrors.append("Text size too small")
            except ValueError:
                self.__pmerrors.append("Text size not an int")
            try:
                ps = int(self.__pmentries[3].get())
                if (ps < 4):
                    self.__pmerrors.append("Preview size too small")
            except ValueError:
                self.__pmerrors.append("Preview size not an int")
            try:
                bh = int(self.__pmentries[4].get())
                if (bh < 1):
                    self.__pmerrors.append("Button height too small")
            except ValueError:
                self.__pmerrors.append("Button height not an int")
            try:
                bw = int(self.__pmentries[5].get())
                if (bw < 1):
                    self.__pmerrors.append("Button width too small")
            except ValueError:
                self.__pmerrors.append("Button width not an int")
            try:
                ti = float(self.__pmentries[6].get())
                if (ti < 0):
                    self.__pmerrors.append("Transparency too small")
                elif (ti > 1):
                    self.__pmerrors.append("Transparency too large")
            except ValueError:
                self.__pmerrors.append("Transparency not a float")

            for i in range(0, 6):
                if len(str(self.__pmentries[self.__startPageIdx + i].get()).split(' ')) > 14:
                    self.__pmerrors.append("Too many in page " + str(i))
                elif len(str(self.__pmentries[self.__startPageIdx + i].get()).split(' ')) < 14:
                    self.__pmerrors.append("Not enough in page " + str(i))
            if len(self.__pmerrors) > 0:
                self.__pmframes.pop()
                self.__pmframes.append(tkinter.Frame(self.__gui))
                err_thread = threading.Thread(target=self.print_errors)
                err_thread.start()
            else:
                self.check_profile()

    def check_profile(self):
            for fn in os.listdir('.'):
                if (str(fn) == ("profile" + str(self.__pmentries[0].get()) + ".txt")):
                    self.__pmwarning = tkinter.Toplevel()
                    self.__pmw_msg = tkinter.Label(self.__pmwarning, text="Do you want to overwrite " +
                                                                      str(fn) + "?", font=self.__pmtextFont)
                    self.__pmw_msg.grid(row=0, columnspan=2, sticky="wens")
                    self.__pmw_cancel = tkinter.Button(self.__pmwarning, text="Cancel",
                                                     font=self.__pmtextFont, command=lambda: self.dialog(False))
                    self.__pmw_confirm = tkinter.Button(self.__pmwarning, text="Confirm",
                                                      font=self.__pmtextFont, command=lambda: self.dialog(True))
                    self.__pmw_cancel.grid(row=4, column=0, sticky="wens")
                    self.__pmw_confirm.grid(row=4, column=1, sticky="wens")

                    self.__pmradioSelect = tkinter.IntVar()
                    self.__pmradioSelect.set(0)
                    self.__pmradioYes = tkinter.Radiobutton(self.__pmwarning,
                                                          text="Clear dictionary",
                                                          font=self.__pmtextFont,
                                                          variable=self.__pmradioSelect,
                                                          value=1).grid(row=1, columnspan=2, sticky="wens")
                    self.__pmradioNo = tkinter.Radiobutton(self.__pmwarning,
                                                         text="Keep dictionary",
                                                         font=self.__pmtextFont,
                                                         variable=self.__pmradioSelect,
                                                         value=0).grid(row=2, columnspan=2, sticky="wens")
                    self.__pmradioAdd = tkinter.Radiobutton(self.__pmwarning,
                                                          text="Append dictionary",
                                                          font=self.__pmtextFont,
                                                          variable=self.__pmradioSelect,
                                                          value=2).grid(row=3, column=0, sticky="wens")
                    self.__pmaddDict = tkinter.StringVar(self.__pmwarning)
                    self.__pmaddDict.set(self.__dict_list[0])
                    self.__pmdictlist = tkinter.OptionMenu(self.__pmwarning,
                                                         self.__pmaddDict,
                                                         *self.__dict_list).grid(row=3, column=1, sticky="wens")

                    self.__pmwarning.columnconfigure(0, weight=1)
                    self.__pmwarning.columnconfigure(1, weight=1)
                    return
            # added a new profile to current directory
            self.__prof_list.append("profile" + str(self.__pmentries[0].get()) + ".txt")
            self.__pmentries[self.__rowCounter - 1].grid_forget()
            self.__pmentries.pop()
            self.__pmentries.append(tkinter.OptionMenu(self.__pmframes[0],
                                                     self.__pmswitchFile,
                                                     *self.__prof_list))
            self.__pmentries[self.__rowCounter - 1].grid(row=self.__rowCounter, column=0,
                                                       sticky="wens")
            self.create_profile(0)

    def dialog(self, response):
        self.__pmwarning.destroy()
        if response is True:
            self.create_profile(int(self.__pmradioSelect.get()))

    def create_profile(self, dictOptIdx):
            # dictOptIdx = 0 if keep dict, 1 if reset dict, 2 if add to dict
            fn_suffix = "profile" + str(self.__pmentries[0].get()) + ".txt"
            with open(fn_suffix, "w") as new_prof:
                # write the non-mapping data
                new_prof.write("dict_" + fn_suffix + '\n' +
                               str(self.__pmentries[1].get()) + '\n' +
                               str(self.__pmentries[2].get()) + " " +
                               str(self.__pmentries[3].get()) + " " +
                               str(self.__pmentries[4].get()) + " " +
                               str(self.__pmentries[5].get()) + " " +
                               str(self.__pmentries[6].get()) + " " +
                               str(self.__pmflash.get()) + " " +
                               str(self.__pmcaps.get()) + " " +
                               str(self.__pmmapidText.get()) + " " +
                               str(self.__pmmapidBg.get()) + " " +
                               str(self.__pmkeyBg.get()) + " " +
                               str(self.__pmkeyText.get()) + " " +
                               str(self.__pmshow.get()))
                # now write the mapping data
                for t in range(0, 6):
                    new_prof.write('\n' + "Switch CapsLock " +
                                   str(self.__pmentries[self.__startPageIdx + t].get()))
            new_prof.close()
            if (dictOptIdx is 1):
                with open("dict_" + fn_suffix, "w") as clear_dict:
                    clear_dict.write("1 1 1")
                clear_dict.close()
            elif (dictOptIdx is 2):
                with open(self.__pmaddDict.get(), "r") as read_otherdict:
                    extras = [line.rstrip('\n') for line in read_otherdict]
                    with open("dict_" + fn_suffix, "a") as append_dict:
                        for i in range(1, len(extras)):
                            append_dict.write('\n' + extras[i])
                    append_dict.close()
                read_otherdict.close()

    def print_errors(self):
        for i in range(0, len(self.__pmerrors)):
            self.__pmerrorLabels.append(tkinter.Label(self.__pmframes[1],
                                                    text=self.__pmerrors[i]))
            self.__pmerrorLabels[i].grid(row=int(i / 3), column=(i % 3), sticky="wens")
        self.__pmframes[1].grid(row=0, sticky="wens")

    def option_change(self, *args):
        contents = self.get_profile_content(self.__pmswitchFile.get())
        self.change_content(contents)

    def get_profile_content(self, file_name):
        # gets information from last used profile
        with open(file_name, "r") as get_prof_con:
            content = [line.rstrip('\n') for line in get_prof_con]
        get_prof_con.close()
        return content

    def change_content(self, content):
            # profile name
            self.__pmentries[0].delete(0, len(self.__pmentries[0].get()))
            temp_file = self.__pmswitchFile.get()
            show_file = temp_file[7:-4]
            self.__pmentries[0].insert(0, show_file)
            # GUI Header
            self.__pmentries[1].delete(0, len(self.__pmentries[1].get()))
            self.__pmentries[1].insert(0, str(content[1]))

            format = [item.rstrip(' ') for item in str(content[2]).split(' ')]

            for q in range(2, 7):
                self.__pmentries[q].delete(0,
                        len(self.__pmentries[q].get()))
                self.__pmentries[q].insert(0, str(format[q - 2]))

            # flash color
            self.__pmflash.set(str(format[5]))

            # caps color
            self.__pmcaps.set(str(format[6]))

            # map id text color
            self.__pmmapidText.set(str(format[7]))

            # map id bg color
            self.__pmmapidBg.set(str(format[8]))

            # map Key bg folor
            self.__pmkeyBg.set(str(format[9]))

            # map key text folor
            self.__pmkeyText.set(str(format[10]))

            # set
            self.__pmshow.set(str(format[11]))

            for i in range(0, 6):
                remove_len = len("Switch CapsLock ")
                temp_string = content[3 + i][remove_len:]
                self.__pmentries[14 + i].delete(0, len(self.__pmentries[14 + i].get()))
                self.__pmentries[14 + i].insert(0, temp_string)


#if __name__ == "__main__":
#    app = LIST_GUI()
#    test = threading.Thread(target=app.testAutoCom,
#                            args=["sample_input1.txt",
#                                  "sample_input2.txt",
#                                  "sample_input3.txt"])
#    test.start()
#    app.run()
