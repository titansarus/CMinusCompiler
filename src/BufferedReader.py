class BufferedReader:
    def __init__(self, filename="input.txt", half_buffer_size=1024):
        self.filename = filename
        self.file = open(filename, 'r')
        self.half_buffer_size = half_buffer_size
        self.buffer = [""] * 2
        self.forward = 0
        self.current_half = 1 # So goto_next_half_buffer goes to 0
        self.must_fill_next_half_buffer = True
        self.goto_next_half_buffer()

    def goto_next_half_buffer(self):
        self.current_half = (self.current_half + 1) % 2
        self.forward = 0
        if self.must_fill_next_half_buffer:
            self.buffer[self.current_half] = self.file.read(self.half_buffer_size)
            self.has_next = (self.buffer[self.current_half] != "")
        self.must_fill_next_half_buffer = True

    def retreat(self):
        if self.forward == 0:
            self.current_half = (self.current_half + 1) % 2
            self.forward = len(self.buffer[self.current_half]) - 1
            self.must_fill_next_half_buffer = False
        else:
            self.forward -= 1

    def next_char(self):
        retval = self.buffer[self.current_half][self.forward]
        self.forward += 1
        if self.forward == len(self.buffer[self.current_half]):
            self.goto_next_half_buffer()
            if not self.has_next:
                self.file.close()
        return retval, self.has_next
