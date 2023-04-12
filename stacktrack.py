from typing import List
from tabulate import tabulate
import random
import string

characters = string.ascii_lowercase

class StackItem:
    def __init__(self, datatype: str, datalen: int, name: str):
        self.datatype = datatype
        self.datalen = datalen
        self.name = name


class Stack:
    def __init__(self, start_index: int, index: int = 0, items: List[StackItem] = [], name: str = ""):
        self.start_index = start_index
        self.index = start_index if index == 0 else index
        self.items = items
        self.loc = 0
        self.offset = 0
        self.name = name if name != "" else ''.join(random.choice(characters) for i in range(5))

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
    
class SessionContext:
    def __init__(self):
        self.selected_stack = None
        self.stacks = {}

    def select_stack(self, sname: str):
        self.selected_stack = self.stacks[sname]

    def add_stack(self, stack: Stack):
        self.stacks[stack.name] = stack

    def sstack_push(self, item: StackItem):
        self.selected_stack.push(item)

    def sstack_pop(self):
        self.selected_stack.pop()

def handle_input(uinput: str, context: SessionContext):
    uinput = uinput.split()
    if len(uinput) < 1:
        print("Please enter a command")
        return ""
    
    if uinput[0] == 'quit':
        return "quit"

    if uinput[0] == 'push':
        dtype = uinput[1]
        dlen = int(uinput[2])
        dname = uinput[3]
        item = StackItem(dtype, dlen, dname)
        context.sstack_push(item)
        return f"pushed {dname} to stack {ctx.selected_stack.name}"
    
    if uinput[0] == 'pop':
        context.sstack_pop()
        return f"popped from stack {ctx.selected_stack.name}"
    
    if uinput[0] == 'select':
        name = uinput[1]
        context.select_stack(name)
        return f"selected stack {name}"
    
    if uinput[0] == 'mkstack':
        name = uinput[1]
        index = uinput[2]
        if '0x' in index:
            index = int(index, 16)
        else:
            index = int(index)
        
        stack = Stack(start_index = index, name=name)
        ctx.add_stack(stack)
        return f"created new stack {name}"
    
    if uinput[0] == "print":
        return ctx.selected_stack.__str__()

    return "command not found"


resp = ""
ctx = SessionContext()
while resp != 'quit':
    uinput = input("> ")
    resp = handle_input(uinput, ctx)
    print(resp)
