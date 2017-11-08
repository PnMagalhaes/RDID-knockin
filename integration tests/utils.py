import sys, glob, serial, serial.tools.list_ports, time
from pynput import keyboard

strokes = []
st = []

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            #for a in serial.tools.list_ports.comports():
                #print(a.hwid)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result[0]


def on_press(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    try:
        strokes.append(time.time())
        # print(' alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        strokes.append(time.time())
        # print(' special key {0} pressed'.format(key))


def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def timmeKeys():
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    a = strokes
    return ([x - a[i - 1] for i, x in enumerate(a)][1:])

if __name__ == '__main__':
    print (serial_ports())