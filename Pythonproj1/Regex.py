import re
#text="this is a good day"
#text1="ACAAAABCBCBAA"

#print(re.search("good",text))
#print(re.search("^this",text))
#print(re.findall("A",text1))
#print(re.findall("[^B]",text1))

with open("Regextest.txt") as file:
    text=file.read()
#print(text)

pattern="(?<=n)([\w\s]*)(\[edit\])"

print(re.findall(pattern,text))
for i in re.finditer(pattern,text):
    print(i.groups())

#assign1
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""
    pattern="[A-Z][a-z]*"
    result=re.findall(pattern,simple_string)

    print(result)
names()

#Assignment2

#import re
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old.
    Ruth and Peter, their parents, have 3 kids."""
    pattern="[A-Z][a-z]*"
    result=re.findall(pattern,simple_string)
    return result
names()

#############################
#import re
def grades():
    with open("assets/grades.txt", "r") as file:
        grades = file.read()

    pattern = "[\w ]+(?=\: B)"
    result = re.findall(pattern, grades)

    return result


grades()
# raise NotImplementedError()


#####################################
#import re

y=[]
def logs():
    with open("logdata.txt", "r") as file:
        logdata = file.read()
    x=re.finditer("(?P<host>([\w]*\.)+([\w]+))(\s-\s)(?P<user_name>[a-z0-9]+|-)(\s\[)(?P<time>[\w]*/[\w]*/[\w]*:[\w]*:[\w]*:[\w]*\s-[\w]*)]\s\"(?P<request>[A-Z]+\s/(([\w(-|+|%)])+|([/\w\s])+)+)",
                logdata)

    for item in x:
        y.append(item.groupdict())
    return y

logs()

assert len(logs()) == 979

one_item={'host': '146.204.224.152',
  'user_name': 'feest6811',
  'time': '21/Jun/2019:15:45:24 -0700',
  'request': 'POST /incentivize HTTP/1.1'}
assert one_item in logs(), "Sorry, this item should be in the log results, check your formating"








# raise NotImplementedError()
