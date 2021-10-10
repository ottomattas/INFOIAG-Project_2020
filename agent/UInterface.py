import os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def userMenu(displayset):
    while(True):
        for index, element in enumerate(displayset):
            print(str(index+1) + ") " + element)
        uinput = input("\nSelect a number: ")
        try:
            uindex = int(uinput) - 1
            if uindex < 0 or uindex >= len(displayset):
                raise Exception("Index Error")
            return uindex
        except:
            print("Please select a number on the list")

def multiUserMenu(displayset, textprompt=None):
    ret = []
    if textprompt is not None:
        print(textprompt)
    while(True):
        for index, element in enumerate(displayset + ["Back/Done"]):
            if index in ret:
                continue
            print(str(index+1) + ") " + element)
        uinput = input("Select a number: ")
        try:
            uindex = int(uinput) - 1
            if uindex == len(displayset):
                return ret
            elif uindex < 0 or uindex > len(displayset) or uindex in ret:
                raise Exception("Index Error")
            else:
                ret.append(uindex)
            clear()
            if textprompt is not None:
                print(textprompt)
        except:
            print("Please select a number on the list")
