from dataclasses import dataclass

@dataclass
class Memory:
    def __init__(self):
        self.kind = ""
        self.name = None
        self.variable = None

    def set(self, kind, name, variable):
        self.kind = kind
        self.name = name
        self.variable = variable