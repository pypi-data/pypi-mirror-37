import serial
import serial.tools.list_ports

class MegaException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)

class ArduinoConnection(object):

    def __init__(self, tty = None, baud = 115200):
        self.serial = None
        self.tty = None
        self.baud = baud
        if (tty is None):
            tty = self.select_tty()
        if tty is not None:
            self.open(tty)

    def ping(self):
        self.serial.write('ping\n')
        line = self.serial.readline()
        if line.find('pong') == -1:
            raise MegaException('Expected pong, got: ' + line)

    def flush(self):
        self.serial.write('\n')
        line = self.serial.readline()

    def write(self, output):
        return self.serial.write(output)

    def readline(self):
        return self.serial.readline()

    def open(self, tty):
        try:
            if self.serial is not None:
                self.serial.close()
            self.tty = tty
            self.serial = serial.Serial(self.tty, self.baud, timeout=1)
            line = self.serial.readline()
            if line.find('Ready') == -1:
                self.flush()
                self.ping()
        except Exception as ex:
            raise MegaException(str(ex))

    def close(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    @classmethod
    def get_ttys(cls):
        return list(serial.tools.list_ports.comports())

    @classmethod
    def print_ttys(cls):
        ports = cls.get_ttys()
        print("[")
        for p in ports:
            try:
                fmt = '  {{ "name" : "{}" , "description" : "{}" , "manufacturer" : "{}" , "serial" : "{}" , "device" : "{}" }},'
                print(fmt.format(p.name, p.description, p.manufacturer, p.serial_number, p.device))
            except:
                pass
        print(']')

    def select_tty(self):
        for p in self.get_ttys():
            try:
                if p.description.find('Arduino') != -1 or \
                   p.manufacturer.find('Arduino') != -1 or \
                   p.manufacturer.find('FTDI') != -1:
                        return p.device
            except:
                pass
        return None


class ArduinoObject(object):

    def __init__(self, conn, name, type):
        self.conn = conn
        self.name = name
        self.type = type

    def do(self, args):
        cmd = 'do {} {}\n'.format(self.name, args)
        self.conn.write(cmd)
        line = self.conn.readline()
        if line.find('do ok') == -1:
            raise MegaException(line)

    def create(self, args):
        cmd = 'create {} as {} {}\n'.format(self.name, self.type, args)
        self.conn.write(cmd)
        line = self.conn.readline()
        if line.find('create ok') == -1:
            raise MegaException(line)

    def get(self, attr):
        cmd = 'get {} {}\n'.format(self.name, attr)
        self.conn.write(cmd)
        line = self.conn.readline()
        return line.rstrip()    # Trim trailing newline and other whitespaces

    def set(self, attr, value):
        cmd = 'set {} {} {}\n'.format(self.name, attr, value)
        self.conn.write(cmd)
        line = self.conn.readline()
        if line.find('set ok') == -1:
            raise MegaException(line)
