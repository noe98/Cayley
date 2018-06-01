# trying to write code to produce excel code

s=50
text= str("=AVERAGE(")
for x in range(0,s-1,1):
    text= str(text+ "'Den "+str(x)+"'!B7,")
text= str(text+ "'Den "+str(s-1)+"'!B7)")

with open("excelhelp.txt", "w") as text_file:
    print("{}".format(text), file=text_file)
