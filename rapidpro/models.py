
class Node:
    pass



class AbstractAction:

    def add_note(self):
        return NotImplementedError

    pass

class SendMessageAction(AbstractAction):
    pass



class AbstractRouter:
    pass

class SwitchRouter:
    pass

class RandomRouter:
    pass

class SaveNameRouter:
    pass
