from micro_ble.ble_helper import BLEHelper
import time


DEVICE = '66b2c551-50df-4188-a436-d6858835fbe0'
DEVICE_LCD = '66b2c551-50df-4188-a436-d6858835fbe2'
DEVICE_BUTTONS = '66b2c551-50df-4188-a436-d6858835fbe1'
SERVICES = {
    DEVICE: [DEVICE_BUTTONS, DEVICE_LCD],
}


class BLE:
    def __init__(self):
        self.menu_callback = None
        self.ble_helper = BLEHelper()
        for service in SERVICES:
            self.ble_helper.support_service(service, SERVICES[service])

        self.lcd = None
        self.cache = {}
        self.mtu = 18

    def scan(self):
        addresses = self.ble_helper.scan()
        self.cache = {}

    def broadcast_to_lcd(self, track_data):
        if not self.ble_helper.enabled:
            return
        data = track_data.get_data()
        for k, v in data.items():
            if k not in self.cache or v != self.cache[k]:
                self.cache[k] = v
                pos = 0
                packet_data = str(v)
                data_chunk = packet_data[0:self.mtu]
                while data_chunk:
                    message = str(track_data.get_code_for_key(k)) + str(pos) + data_chunk
                    self.ble_helper.broadcast(DEVICE_LCD, message)
                    pos += 1
                    data_chunk = str(v)[pos*self.mtu:(pos+1)*self.mtu]

    def get_data(self):
        return self.ble_helper.get_data()

ble = BLE()
ble.scan()

try:
    while True:
        reads = ble.get_data()
        for uuid in reads:
            if reads[uuid] is not None:
                print(reads[uuid])
        time.sleep(1)

except KeyboardInterrupt:
    pass
