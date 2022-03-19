from enum import Enum



'''
Перечисление, которое описывает все возможные состояния в боте
''' 
class State(Enum):
    Nope = 0
    Start = 1
    CreateTopic = 2
    CreateMessage = 3
    CreateAnswer = 4
    

'''
Класс описывает объект, который хранит текущее состояние для конктретного пользователя
''' 
class UserState:
    

    id = ""
    state = State.Nope
    
    def __init__(self, id) -> None:
        self.id = str(id)
        self.state = State.Nope
    
    def SetState(self, newState: State) -> None:
        self.state = newState
        
    def GetState(self) -> State:
        return self.state


'''
Класс описывает хранилище, которое хранит текущее состояние для всех пользователей. 
доступ происходит по идентификатору пользователя
'''
class StateMachine:
    
    allUsers = dict()
    
    def AddUser(self, id) -> None:
        self.allUsers[str(id)] = UserState(id)
    
    def SetState(self, id, state : State) -> None:
        if(str(id) not in self.allUsers.keys()):
            self.AddUser(id)
        self.allUsers[str(id)].SetState(state)
        
    def GetState(self, id) -> State:
        if(not self.ContainsUser(id)):
            self.AddUser(id)  
        return self.allUsers[str(id)].GetState()              
            
    def ContainsUser(self, id) -> bool:
        return str(id) in self.allUsers.keys()   