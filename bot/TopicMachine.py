'''
Класс описывает объект, который хранит текущее состояние для конктретного пользователя
'''


class UserState:
    id = ""
    state = None

    def __init__(self, id) -> None:
        self.id = str(id)
        self.state = None

    def SetState(self, newState) -> None:
        self.state = newState

    def GetState(self) -> int:
        return self.state


'''
Класс описывает хранилище, которое хранит текущее состояние для всех пользователей. 
доступ происходит по идентификатору пользователя
'''


class TopicMachine:
    allUsers = dict()

    def AddUser(self, id) -> None:
        self.allUsers[str(id)] = UserState(id)

    def SetState(self, id, state: int) -> None:
        if (str(id) not in self.allUsers.keys()):
            self.AddUser(id)
        self.allUsers[str(id)].SetState(state)

    def GetState(self, id) -> int:
        if (not self.ContainsUser(id)):
            self.AddUser(id)
        return self.allUsers[str(id)].GetState()

    def ContainsUser(self, id) -> bool:
        return str(id) in self.allUsers.keys()
