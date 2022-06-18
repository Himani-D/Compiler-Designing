roll = int(input("Enter your rollno."))
if(roll%2==0 and roll<=100):
    print()
    print("You are entering into Blue Zone.")
    name = input().lower()
    if(ord(name[0])<=ord('m')):
        print("Your group is warriors!")
    else:
        print("Your group is achievers!")
else:
    print("You are entering into Green Zone.")
    name = input().lower()
    if(ord(name[0])<=ord('m')):
        print("Your group is warriors!")
    else:
        print("Your group is achievers!")