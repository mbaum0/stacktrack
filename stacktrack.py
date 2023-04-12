from typing import List
from tabulate import tabulate

class StackItem:
    def __init__(self, datatype: str, datalen: int, name: str):
        self.datatype = datatype
        self.datalen = datalen
        self.name = name


class Stack:
    def __init__(self, start_index: int, index: int = 0, items: List[StackItem] = []):
        self.start_index = start_index
        self.index = start_index if index == 0 else index
        self.items = items
        self.loc = 0
        self.offset = 0

    def push(self, stack_item: StackItem):
        self.items.append(stack_item)
        stack_item.loc = self.index
        stack_item.offset = self.index - self.start_index
        self.index -= stack_item.datalen

    def pop(self):
        item = self.items.pop()
        self.index += item.datalen

    def __str__(self):
        table_data = [[hex(i.loc), hex(i.offset), i.name, i.datatype, i.datalen] for i in reversed(self.items)]
        headers = ["Loc", "Offset", "Name", "Type", "Length"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")

        stack_info = f"Stack Pointer:\t\t{hex(self.index)}\nStack Base Pointer:\t{hex(self.start_index)}\n"
        return stack_info + table
    

stack = Stack(0x100)

int1 = StackItem("int", 4, "x")
int2 = StackItem("int", 4, "y")
int3 = StackItem("int", 4, "z")
char1 = StackItem("char*", 8, "ptr_0")
char2 = StackItem("char*", 8, "ptr_1")
char3 = StackItem("char*", 8, "ptr_2")

stack.push(int1)
stack.push(int2)
stack.push(int3)
stack.push(char1)
stack.push(char2)
stack.push(char3)

print(stack)

stack.pop()
stack.push(int1)

print(stack)