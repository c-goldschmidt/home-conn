
class SpotifyDevices:
    def __init__(self):
        self.known_devices = []

    def update(self, device_list):
        new_ids = [dev['id'] for dev in device_list]
        self.known_devices = [{
            **dev,
            'is_active': False,
            'is_available': False,
        } for dev in self.known_devices if dev['id'] not in new_ids]
        self.known_devices = [*self.known_devices, *[
            {**dev, 'is_available': True} for dev in device_list
        ]]
