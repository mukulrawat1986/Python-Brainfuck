import sys

class Brainfry(object):
    
    def __init__(self):
        # we simulate the array with a list
        # the array has a capacity of 30,000 byte cells
        self.array = [0]*(30*10**3)
        # the data pointer, initially at position 0
        self.dataptr = 0
        # dictionary that maps the '[' with index of corresponding ']' and
        # ']' with the index of corresponding '['
        self.mapBrackets = {}
        

    def lt(self):
        """Function to simulate the '<' command.
        The '<' operator decrements the data pointer,
        we have to make sure the data pointer is not negative"""
        if self.dataptr <= 0:
            raise ValueError, "Operation making data pointer go beyond min array limit"
        self.dataptr -= 1

    def gt(self):
        """Function to simulate the '>' command.
        The '>' command increments the data pointer,
        we have to make sure it doesn't crosses the array limit
        """
        if self.dataptr >= (30*10**3) - 1:
            raise ValueError, "Operation making data pointer go beyond max array limit"
        self.dataptr += 1

    def add(self):
        """Function to simulate the '+' command.
        The '+' command increments the byte at the data pointer by 1.
        We have to make sure there is no overflow of value, since characters can have value in range 0 to 255
        """
        self.array[self.dataptr] = (self.array[self.dataptr] + 1) % 256

    def sub(self):
        """Function to simulate the '-' command.
        The '-' command decrements the byte at the data pointer by 1.
        Just like add, we have to make sure there is no underflow of value."""
        self.array[self.dataptr] = (self.array[self.dataptr] - 1) % 256

    def stop(self):
        """Function to simulate the '.' command.
        The '.' command outputs the byte at the data ptr.
        We use chr function since we are storing the ascii value in our array."""
        sys.stdout.write(chr(self.array[self.dataptr]))

    def comma(self):
        """Function to simulate the ',' command.
        The ',' command accepts one byte of input, storing its value in the byte at the data pointer.
        We have to make sure that we stop accepting input at EOF.
        Note: """
        t = ord(sys.stdin.read(1))
        if t != 26:
            self.array[self.dataptr] = t

    def mapTheBrackets(self, bfcode):
        """The '[' and ']' command can be used as while loops in the brainfuck code.
        If the value in current cell is greater than 0, '[' command makes it go to the next instruction else jump to closing ']'
        The ']' command makes the instruction pointer go to opening '[' 
        """
        stack = []

        for index, instruction in enumerate(bfcode):
            if instruction == '[':
                # store index of '['
                stack.append(index)
            elif instruction == ']':
                try:
                    start = stack.pop()
                    # map index of '[' to index of ']'
                    self.mapBrackets[start] = index
                    # map index of ']' to index of '['
                    self.mapBrackets[index] = start
                except IndexError:
                    # In case the stack is empty
                    raise ValueError, "more ] than ["

        # at the end of code, the stack must be empty
        if stack != []:
            raise ValueError, "more [ than ]"

    def cleanupcode(self, bfcode):
        """Function to remove all extra characters from the Brainfuck code"""
        return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-' ], bfcode)

    def evaluatecode(self, bfcode):
        """Function to evaluate the brainfuck code"""
        # map all commands other than '[' and ']' to the associate functions
        mapFunctions = { '<': self.lt,
                         '>': self.gt,
                         '+': self.add,
                         '-': self.sub,
                         '.': self.stop,
                         ',': self.comma
                         }

        # clean the code to remove all extra characters
        bfcode = self.cleanupcode(list(bfcode))

        # map the indices of '[' to indices of ']' and viceversa
        self.mapTheBrackets(bfcode)

        # initialize the program counter, to move over all the code
        pc = 0

        # This loop runs till the end of code
        while pc < len(bfcode):

            instruction = bfcode[pc]
            
            # if instruction is a command present in mapFunctions, call it
            if instruction in mapFunctions:
                apply(mapFunctions[instruction])
            elif instruction == '[':
                # if byte at data pointer is zero jump forward to command after matching ']'
                if self.array[self.dataptr] == 0:
                    # go to the index of matching ']'
                    pc = self.mapBrackets[pc]
            elif instruction == ']':
                # jump to the corresponding starting position
                pc = self.mapBrackets[pc] - 1
                # here pc is the position of the ']'
            
            # increment the program counter
            pc += 1
        

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        raise ValueError,  'Usage Error'
    
    filename = sys.argv[1]
    
    with open(filename, "r") as f:
        # read the brainfuck code
        bfcode = f.read()
        
        # Create an instance of the Brainfry class
        B = Brainfry()

        # Evaluate the Brainfuck code
        B.evaluatecode(bfcode)

