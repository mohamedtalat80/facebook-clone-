decode = {".-": "A",
          "-...": "B",
          "-.-.": "C",
          "-..": "D",
          ".": "E",
          "..-.": "F",
          "--.": "G",
          "....": "H",
          "..": "I",
          ".---": "J",
          "-.-": "K",
          ".-..": "L",
          "--": "M",
          "-.": "N",
          "---": "O",
          ".--.": "P",
          "--.-": "Q",
          ".-.": "R",
          "...": "S",
          "-": "T",
          "..-": "U",
          "...-": "V",
          ".--": "W",
          "-..-": "X",
          "-.--": "Y",
          "--..": "Z",
          "-----": "0",
          ".----": "1",
          "..---": "2",
          "...--": "3",
          "....-": "4",
          ".....": "5",
          "-....": "6",
          "--...": "7",
          "---..": "8",
          "----.": "9"}
def decode_morse(morse_code):
    res=""
    for i in morse_code.split(" "):
        if i == " ":
            res ="".join(res.replace(""," "))
        else:
            res ="".join(res.replace(i,decode[i]))
    return res
print(decode_morse(".... . -.--   .--- ..- -.. .") )    
           
#     return "".join([decode[i] if i in decode else " " for i in morse_code.split(" ")]).replace("  ", " ")
# print(decode_morse(".... . -.--   .--- ..- -.. .") )
