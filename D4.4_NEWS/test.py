import re

CENSORED_WORDS = {
    'fuck': '****',
    'shit': '****',
    'cunt': '****',
    'ass': '***',
    'piss': '***',
    'bastard': '*******'
}

def censor(value):
    temp = value
    for word in CENSORED_WORDS.keys():
        test = re.compile(re.escape(word), re.IGNORECASE)
        result = test.sub(CENSORED_WORDS[word], temp)
        temp = str(result)
    return temp

string = "I like to FuCk but no french letter, sHit, BasTard, dumbaSS, piss, CUNT."
string = censor(string)

print(string)