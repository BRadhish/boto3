action = input('Enter your action:')

#print(action)
def main(action):
    if action == "create":
        create()
    elif action == "update":
        update()
    elif action == "start":
        start()
    else:
        print("action is not available")

def create():
    print("create")
    #return create;
    

def update():
    print("update")
    return update;

def start():
    print("start")
    return start;

def stop():
    print("stop")
    return stop;


if __name__ == "__main__":
    main(action)
