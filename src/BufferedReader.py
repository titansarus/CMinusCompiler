class BufferedReader:
    def __init__(self, filename="input.txt", half_buffer_size=1024):
        self.filename = filename
        self.file = open(filename, 'r')
        self.half_buffer_size = half_buffer_size
        self.buffer = [''] * ((self.half_buffer_size + 1) * 2)
        self.forward = 0
        read_string = self.file.read(self.half_buffer_size)
        self.ending_retreat = False
        self.buffer[:len(read_string)] = read_string

    def fill_buffer(self, read_string, half):
        if half == 1:
            for i in range(len(read_string)):
                self.buffer[i] = read_string[i]
            self.buffer[len(read_string)] = ''
        elif half == 2:
            for i in range(len(read_string)):
                self.buffer[i + self.half_buffer_size + 1] = read_string[i]
            self.buffer[len(read_string) + self.half_buffer_size + 1] = ''

    def retreat(self):
        if self.forward == self.half_buffer_size + 1:
            self.forward -= 1
            self.ending_retreat = True
        if self.forward == 0:
            self.forward = self.half_buffer_size * 2 + 1
            self.ending_retreat = True
        self.forward -= 1

    def next_char(self):
        retval = self.buffer[self.forward]
        self.forward += 1
        if not self.ending_retreat:
            if self.buffer[self.forward] == '':
                if self.forward == self.half_buffer_size:
                    read_string = self.file.read(self.half_buffer_size)
                    self.fill_buffer(read_string, 2)
                    self.forward += 1
                    if read_string == '':
                        self.file.close()
                        return retval, False
                elif self.forward == self.half_buffer_size * 2 + 1:
                    read_string = self.file.read(self.half_buffer_size)
                    if read_string == '':
                        self.file.close()
                        return retval, False
                    self.fill_buffer(read_string, 1)
                    self.forward = 0
                else:
                    self.file.close()
                    return retval, False
        else:
            if self.forward == self.half_buffer_size:
                self.forward += 1
                self.ending_retreat = False
            elif self.forward == self.half_buffer_size * 2 + 1:
                self.forward = 0
                self.ending_retreat = False
            else:
                raise Exception("Should Not Reach this state")
        return retval, True
