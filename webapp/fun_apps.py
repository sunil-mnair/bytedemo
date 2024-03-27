from datetime import datetime,timedelta
import pyqrcode, png,random,os

def find_vowels(word,vowels):
    for letter in word:
        if letter in vowels:
            vowels[letter] += 1
    return vowels

def find_words(lettersinput,wordlist):

    letters = [letterinput for letterinput in lettersinput]
    answers=[]
    max_length = ""
    word_cookies=[{}]

    def checkword(word):
        localletters=letters.copy()
        wordanswer = True
        for letter in word:
            if letter in localletters:
                localletters.remove(letter)
            else:
                wordanswer=False
                break
        if wordanswer == True:
            answers.append(word)

    #with app.open_resource('static/engmix.txt') as file:
    #with open('engmix.txt','r') as file:
        #wordlist = file.readlines()

    for word in wordlist:
        word = word.decode()
        word = word.rstrip("\n")
        checkword(word)

    finalanswers = []
    longestword=0
    for answer in answers:
        length = len(answer)
        if length > longestword:
            longestword=length


    for x in range(longestword+1):
        finalanswers.append([])

    for answer in answers:
        finalanswers[len(answer)-1].append(answer)

    max_length += f"The max length of words possible is {longestword} letters long"

    for index, list in enumerate(finalanswers,1):
        if index != len(finalanswers):
            if list:
                word_cookies[0][index] = []
                list.sort()
                for word in list:
                    word_cookies[0][index].append(f'{word}')

    print(word_cookies)
    #word_cookies = word_cookies.split('\n')
    return max_length,word_cookies

def jumble(sentence):


  sentence = sentence.split()

  new_sentence = []

  for word in sentence:

    positions = list(range(1,len(word)-1))

    jumble = ''

    if len(word) == 3:
        jumble += word[0]
        jumble += word[2]
        jumble += word[1]

        new_sentence.append(jumble)

    elif len(word) == 4:
        jumble += word[0]
        jumble += word[2]
        jumble += word[1]
        jumble += word[3]

        new_sentence.append(jumble)

    elif len(word) > 4:
        jumble += word[0]
        for _ in word[1:-1]:
            index = random.choice(positions)
            jumble += word[index]
            positions.remove(index)

        jumble += word[-1]

        if jumble == word:
            jumble(word)
        else:
            new_sentence.append(jumble)
    else:
        new_sentence.append(word)

    file_path = os.getcwd()+'/mysite/text_files/'

    with open(file_path+"typoglycemia.txt","a") as f:
        f.write(" ".join(sentence) + '\n')
        f.write(" ".join(new_sentence) + '\n')

  return " ".join(new_sentence)

# from pyqrcode import QRCode
def qr_code_generator(s):

    # Generate QR code
    url = pyqrcode.create(s)

    # Create and save the svg file naming "myqr.svg"
    url.svg("myqr.svg", scale = 8)

    # Create and save the png file naming "myqr.png"
    url.png('myqr.png', scale = 6)

    return url


def converttojulian (D,M,Y):
    # The Julian Date value is calculated for the given day, month and year using the following steps
    A = Y / 100
    B = A / 4
    C = 2 - A + B
    E = 365.25 * (Y + 4716)
    F = 30.6001 * (M + 1)
    JD = C + D + E + F - 1524.5
    # since no time has been specified, the JD variable is modified to show exactly 00:00 on the specified date
    return(int(JD) + 0.5)

def datetophase(D,M,Y):
    JD = converttojulian(D,M,Y)
    dayssince = JD - 28.4766799998
    #Here the number starting with 28 is the julian date of the Earliest New Moon in Julian Dates
    numberofnewmoons = dayssince / 29.53

    #This determines the Julian Date of the last new moon before the specified date
    #Using that date, it determines the dates of the rest of the stages.
    lastnewmoon = ((int(numberofnewmoons)) * 29.53) + 28.4766799998
    fullmoon = lastnewmoon + 14.765
    firstquarter = (lastnewmoon + 7.3825)
    thirdquarter = (lastnewmoon + 22.1475)
    nextnewmoon = lastnewmoon + 29.53


    #These if statements determine if any of the 4 phases occurs on any the date specified.
    if (lastnewmoon >= JD and lastnewmoon < (JD + 1))or(nextnewmoon >= JD and nextnewmoon < (JD + 1)):
        return ('new moon'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/newmoon.png')
    elif firstquarter >= JD and firstquarter < (JD + 1):
        return ('first quarter'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/firstquarter.png')
    elif fullmoon >= JD and fullmoon < (JD + 1):
        return ('full moon'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/fullmoon.png')
    elif thirdquarter >= JD and thirdquarter < (JD + 1):
        return ('third quarter'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/thirdquarter.png')
    #If any of those 4 phases do not occur on this date, these if statements determine what phases this date is in between
    elif lastnewmoon < JD and firstquarter >= (JD + 1):
        return ('waxing crescent'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/waxingcrescent.png')
    elif firstquarter < JD and fullmoon >= (JD + 1):
        return ('waxing gibbous'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/waxinggibbous.png')
    elif fullmoon < JD and thirdquarter >= (JD + 1):
        return ('waning gibbous'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/waninggibbous.png')
    elif thirdquarter < JD:
        return ('waning crescent'.title(),'https://github.com/prateetisaran/Moonphasecalculator/raw/master/waningcrescent.png')


def specificdate(x):
    #These get the date entered by the user and split it into 3 seperate values to be used for the calculation.

    specificdate = datetime.strptime(x,"%Y-%m-%d")
    specificdate = specificdate.strftime('%d %B %Y')

    Y = int(x[0:4])
    M = int(x[5:7])
    D = int(x[8:])

    moon_phase = datetophase(D,M,Y)

    return moon_phase,specificdate

    # toprint.set(moon_phase)

    # #These set up the corresponding image to be displayed based on the value obtained by the calculations.
    # moon_phase = displayimage(moon_phase)
    # moon_phase = ImageTk.PhotoImage(Image.open(moon_phase))
    # imgLabel.configure(image=moon_phase)
    # imgLabel.photo = moon_phase


def nextphasefm():
    x = datetime.now()
    c = datetophase((int(x.strftime('%d'))), (int(x.strftime('%m'))), (int(x.strftime('%Y'))))
    D = int(x.strftime('%d'))
    M = int(x.strftime('%m'))
    Y = int(x.strftime('%Y'))
    JD = converttojulian(D,M,Y)
    dayssince = JD - 28.4766799998
    numberofnewmoons = dayssince / 29.53
    lastnewmoon = ((int(numberofnewmoons)) * 29.53) + 28.4766799998
    fullmoon = lastnewmoon + 14.765
    fullmoondate = fullmoon - JD

    if fullmoon > JD:
        fm = datetime.now() + timedelta(days=fullmoondate)
        fm = fm.strftime('%d %B %Y')

    elif fullmoon < JD:
        fm = datetime.now() + timedelta(days=fullmoondate) + timedelta(days=29.53)
        fm = fm.strftime('%d %B %Y')

    elif c[0] == 'Full Moon':
        fm = datetime.now()
        fm = fm.strftime('%d %B %Y')

    return fm

def nextphasenm():
    x = datetime.now()
    c = datetophase((int(x.strftime('%d'))), (int(x.strftime('%m'))), (int(x.strftime('%Y'))))
    D = int(x.strftime('%d'))
    M = int(x.strftime('%m'))
    Y = int(x.strftime('%Y'))
    JD = converttojulian(D,M,Y)
    dayssince = JD - 28.4766799998
    numberofnewmoons = dayssince / 29.53
    lastnewmoon = ((int(numberofnewmoons)) * 29.53) + 28.4766799998
    nextnewmoon = lastnewmoon + 29.53
    newmoondate = nextnewmoon - JD

    if c[0] == 'New Moon':
        nm = datetime.now()
        nm = nm.strftime('%d %B %Y')
    else:
        nm = datetime.now() + timedelta(days=newmoondate)
        nm = nm.strftime('%d %B %Y')

    return nm