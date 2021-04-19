import wolframalpha
import wikipedia
import PySimpleGUI as sg
import pyttsx3

# accessing wolframalpha through an API key
wolfClient = wolframalpha.Client("3LQTUX-9UJKER9246")

# list of mathematical keywords
mathKeywords = ["derivative", "integral", "slope", "times", "plus", "minus", "radius", "multiplied", "divided",
                "power of", "root of", "squared", "cubed", "factorial", "log of", "logarithm", "log base"]

# list of mathematical operators
mathOps = ['+','-','*','/','^','%']

# set GUI theme
sg.theme("DarkBlue")
# Layout the window's contents
layout = [[sg.Text("Enter a command...")],
          [sg.Input()],
          [sg.Button('Enter'), sg.Button("Close")]]
# Create the window
window = sg.Window('ULTRON', layout)

# initializing TTS voice
voice = pyttsx3.init()

# Annnounces itself to user
voice.say("I am ULTRON, your virtual assistant. What can I do for you today Sir?")
voice.runAndWait()

# loop that runs the command
while True:
    event, values = window.read()
    if event in "Close":
        break

    # checking if input contains keywords or is completely numeric (will only use wolfram to solve)
    tempStr = ""
    for i in values[0].split():
        if i in mathKeywords or i in mathOps or i.isdigit():
            tempStr += i
        else:
            break

    if values[0].isdecimal() and mathOps in values[0]:
        # run wolfram only
        res = wolfClient.query(values[0])
        wolfRes = next(res.results).text

        sg.popup(wolfRes)
        continue

    # for key in mathKeywords:
    #     if key in values[0]:
    #         # run wolfram only
    #         break

    # checking query against wolfram
    wolfRes = ""
    try:
        res = wolfClient.query(values[0])
        wolfRes = next(res.results).text
    except:
        wolfRes = "We have no information on this topic."
        sg.PopupNonBlocking(wolfRes)
        voice.say(wolfRes)
        voice.runAndWait()
        continue

    # checking query against wikipedia
    wikiRes = ""
    try:
        wikiRes = wikipedia.summary(values[0], sentences=2)
    except:
        wikiRes = "No additional information on " + values[0]

    # display query's response in popup window
    sg.PopupNonBlocking(wolfRes, wikiRes)

    # text to speech for results
    voice.say(wolfRes)
    voice.runAndWait()

# Close GUI
window.close()
