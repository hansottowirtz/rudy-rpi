class Parking:
    def __init__(self, messenger):
        self.messenger = messenger

    def park(self):
        self.messenger.send('S500')
        self.messenger.send('M550')
        self.hall_count = 0
        while True:
            ln = self.messenger.port.readline()
            if 'H' in ln:
                self.hall_count += 1
            elif ln[0:1] == 'D':
                if ln[0:2] == 'D1':
                    if int(ln[2:5]) > 30:
                        break
        self.messenger.send('M500')
