#   Aim:
#   (A) Read the Research paper provided to understand the use of SDTS in language translation from English to Hindi.
#   (B) Write a program to implement tokenizer, syntax analyzer, and to perform syntax directed translation for conversion
#  from English to Hindi as per the research paper. Also extend the procedure to generate correct Hindi sentence.

#  1. Take input from user and store into file sand extract words and punctuation amd store in array



sent = ["Rose is red in color", "My name is Himani"]
sentences = {}
for s in range(len(sent)):
    sentences[sent[s]] = []

# sent = "गुलाब लाल रंग का है"
dictionary = {"rose":"गुलाब", "red":"लाल", "color":"रंग","name":"नाम", "himani":"हिमानी", "my":"मेरा", "in":"का","is":"है", "car":"गाड़ी","this":"यह", "man":"पुरुष","purple":"बैंगनी","has":"के पास"}
subject =["himani","my","rose","this"]
object=["color"]
verb=["is","in"]
rules = {"subject":subject, "object":object,"verb":verb}
def tokenize(sent):
    return sent.lower().split()

rules = ""
def convert(sent):
    val = tokenize(sent)
    res = ""
    last=[]
    for i in range(len(val)):
        if(val[i] in dictionary.keys()):
            if(val[i] in verb):
                last.append(val[i])
            else:
                res+=dictionary[val[i]]+" "

    for i in last[::-1]:
        res+=dictionary[i]+" "

    
    if("है" not in res):
        res+=" है|"
    else:
        res+="|"
    print(res)

inp=input()
convert(inp)

# This is a car
# My name is Himani
# ROse is red in color
# This man has purple car