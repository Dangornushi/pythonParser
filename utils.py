from node import Node

def printNode(node, callCount=0):
    callCount += 1
    print(node.get_kind())

    if type(node.get_lhs()) == Node and node.get_kind() == "FUNCTION":
        for i in range(node.get_rhs().__len__()):
            printNode(node.get_rhs()[i])
    elif node.get_kind() == "CONDITION":
        for i in range(node.get_lhs().__len__()):
            for i in range(callCount):
                print("  ", end="")
            printNode(node.get_lhs()[i], callCount)

    else:
        if type(node.get_lhs()) == Node:
            for i in range(callCount):
                print("  ", end="")
            print("L: ", end="")
            printNode(node.get_lhs(), callCount)
        elif node.get_lhs() is not None:
            for i in range(callCount):
                print("  ", end="")
            print("L: ", node.get_lhs())

        if type(node.get_rhs()) == Node:
            for i in range(callCount):
                print("  ", end="")
            print("R: ", end="")
            printNode(node.get_rhs(), callCount)
        elif node.get_rhs() is not None:
            for i in range(callCount):
                print("  ", end="")
            print("R: ", node.get_rhs())

    callCount -= 1