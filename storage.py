class Node:
    def __init__(self, fecha, user_r, user_a, errorCode, errorDesc):
        self.fecha = fecha
        self.error = {errorCode:1}
        self.users_R = {user_r:1}
        self.users_A = set(user_a)
        self.reports = 1
        self.next = None

    
    def actualizar(self, user_r, user_a, errorCode, errorDesc):
        self.reports+=1
        if(user_r in self.users_R):
            self.users_R[user_r]+=1
        else:
            self.users_R[user_r] = 1
        
        for user in user_a:
            self.users_A.add(user)

        if(errorCode in self.error):
            self.error[errorCode]+=1
        else:
            self.error[errorCode] = (1)

    
class Lista_Simple:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add(self, fecha,user_Reported,users_Affected,errorCode,errorDesc):
        if(self.head == None):
            newNode = Node(fecha, user_Reported, users_Affected, errorCode, errorDesc)
            self.head = newNode
        elif(self.tail == None):
            if(self.head.fecha == fecha):
                self.head.actualizar(user_Reported, users_Affected, errorCode, errorDesc)
            else:
                newNode = Node(fecha, user_Reported, users_Affected, errorCode, errorDesc)
                self.tail = newNode
                self.head.next = self.tail
        else:
            temp = self.head
            found = False
            while(temp != None):
                if(temp.fecha == fecha):
                    temp.actualizar(user_Reported, users_Affected, errorCode, errorDesc)
                    found = True
                    break
                temp = temp.next
            if(found==False):
                newNode = Node(fecha, user_Reported, users_Affected, errorCode, errorDesc)
                self.tail.next = newNode
                self.tail = newNode
    
    def out(self):
        temp = self.head
        while(temp != None):
            print(temp.fecha)
            print(temp.users_R)
            print(temp.users_A)
            print(temp.error)
            temp = temp.next
