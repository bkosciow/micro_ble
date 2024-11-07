from .ble_scanner import *
from .ble_device_manager import DeviceManager

logger = logging.getLogger(__name__)


class BLEHelper:
    def __init__(self, sleep=10):
        self.device_manager = DeviceManager()
        self.scaner = Scanner(self.device_manager, _sleep=sleep)

        self.lock = False
        self.enabled = True

    def get_lock(self):
        while self.lock:
            time.sleep(0.01)
        self.lock = True

    def release_lock(self):
        self.lock = False

    def support_service(self, service, characteristics):
        self.device_manager.support_service(service, characteristics)

    def get_data(self):
        if not self.enabled:
            return {}
        self.get_lock()
        try:
            reads = self.device_manager.get_notifications(0.100)
        except Exception as e:
            reads = {}

        self.release_lock()
        return reads

    def broadcast(self, characteristic, message):
        if not self.enabled:
            return
        if type(message) is not bytes:
            message = bytes(message, "utf-8")
        self.get_lock()
        self.device_manager.write_to_characteristic(characteristic, message)
        self.release_lock()

    def scan(self, devices=None):
        self.enabled = False
        discovered = self.scaner.scan(devices)
        self.enabled = True
        return discovered

    def count_devices(self):
        return self.device_manager.count_devices()
