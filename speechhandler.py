from threading import Timer
import re
import requests

awake = False
def resetAwake():
    global awake
    print('Neptune sleeping')
    awake = False

def handleSpeech(speech):
    global awake
    if awake:
        print('Result:', speech)
        parseSpeech(speech)
    elif speech == "NEPTUNE":
        awake = True
        print('Neptune Awakened')
        Timer(5.0, resetAwake).start()
    return

def parseSpeech(speech):
    matches = re.match( r'WATER( THE)?\s*(.*)SIDES? FOR\b(.+(MINUTE|SECOND))', speech, re.M|re.I)
    if matches:
        print("Sides: ", matches.group(2))
        print("Time: ", matches.group(3))
        print("/open/" + text2solenoid(matches.group(2)) + "/time/" + str(text2millis(matches.group(3))))
        r = requests.get("http://openwater.raceconditions.net:5000" + "/open/" + text2solenoid(matches.group(2)) + "/time/" + str(text2millis(matches.group(3))))
        print(r.text);

def text2solenoid(text):
    if text.count("LEFT") > 0:
        return "18"
    elif text.count("RIGHT") > 0:
        return "16"
    elif text.count("BOTH") > 0:
        return "all"

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.lower().split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def text2millis(text):
    minutes = text.count("MINUTE")
    seconds = text.count("SECOND")
    number = text2int(text.replace("MINUTE","").replace("SECOND",""))

    if minutes > 0:
        return number * 60 * 1000
    elif seconds > 0:
        return number * 1000


#parseSpeech("WATER THE LEFT SIDE FOR FORTY SECONDS")
#parseSpeech("WATER BOTH SIDE FOR FIVE SECONDS")
#parseSpeech("WATER THE RIGHT SIDES FOR FORTY SECOND")
#parseSpeech("WATER THE LEFT SIDE FOR THIRTY FIVE SECONDS")
#parseSpeech("WATER THE LEFT SIDE FOR FORTY SECONDS")
#parseSpeech("WATER THE LEFT SIDE FOR ONE MINUTE")
#parseSpeech("WATER THE LEFT SIDE FOR TWO MINUTES")
