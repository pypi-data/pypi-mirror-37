import serial
import serial.tools.list_ports

class ArduinoConnection(object):

    def __init__(self, tty = None, baud = 115200):
        if (tty is None):
            self.select_tty()
        else:
            self.tty = tty
        self.baud = baud
        self.serial = serial.Serial(self.tty, baud, timeout=1)
        line = self.serial.readline()
        if line.find('Ready') == -1:
            self.flush()
            self.ping()

    def ping(self):
        self.serial.write('ping\n')
        line = self.serial.readline()
        if line.find('pong') == -1:
            raise Exception('Expected pong, got: ' + line)

    def flush(self):
        self.serial.write('\n')
        line = self.serial.readline()

    def write(self, output):
        return self.serial.write(output)

    def readline(self):
        return self.serial.readline()

    def close(self):
        self.serial.close()

    def select_tty(self):
        ports = list(serial.tools.list_ports.comports())
        selected = None
        print("Availble devices: [")
        for p in ports:
            fmt = '  {{ "name" : "{}" , "description" : "{}" , "manufacturer" : "{}" , "serial" : "{}" , "device" : "{}" }},'
            print(fmt.format(p.name, p.description, p.manufacturer, p.serial_number, p.device))
            if selected is None:
                if p.description.find('Arduino') != -1 or p.manufacturer.find('Arduino') != -1:
                    selected = p
        print(']')

        if selected:
            print("Picking device: {} (serial: {})".format(selected.device, selected.serial_number))
            self.tty = selected.device
        else:
            raise Exception("No connected Arduino devices found")


class ArduinoObject(object):

    def __init__(self, conn, name, type):
        self.conn = conn
        self.name = name
        self.type = type

    def do(self, args):
        cmd = 'do {} {}\n'.format(self.name, args)
        #print cmd
        self.conn.write(cmd)
        line = self.conn.readline()
        if line.find('do ok') == -1:
            raise Exception(line)

    def create(self, args):
        cmd = 'create {} as {} {}\n'.format(self.name, self.type, args)
        #print cmd
        self.conn.write(cmd)
        line = self.conn.readline()
        if line.find('create ok') == -1:
            raise Exception(line)

    def get(self, attr):
        cmd = 'get {} {}\n'.format(self.name, attr)
        #print cmd
        self.conn.write(cmd)
        line = self.conn.readline()
        return line.rstrip()    # Trim trailing newline and other whitespaces

    def set(self, attr, value):
        cmd = 'set {} {} {}\n'.format(self.name, attr, value)
        #print cmd
        self.conn.write(cmd)
        line = self.conn.readline()
        if line.find('set ok') == -1:
            raise Exception(line)
