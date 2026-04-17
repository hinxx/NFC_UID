import time
from packaging.version import parse as parse_version
import os
try:
    from smartcard.CardType import AnyCardType
    from smartcard.CardRequest import CardRequest
    from smartcard.Exceptions import CardRequestTimeoutException
    from smartcard.util import toHexString
except ImportError:
    os.system('python -m pip install pyscard')
try:
    import requests
except ImportError:
    os.system('python -m pip install requests')
    os.system('python -m pip install urllib3==1.26.15')
try:
    import keyboard as Keyboard
except ImportError:
    os.system('python -m pip install keyboard')
try:
    import keyboard as Keyboard  
    import requests
    from smartcard.CardType import AnyCardType
    from smartcard.CardRequest import CardRequest
    from smartcard.Exceptions import CardRequestTimeoutException
    from smartcard.util import toHexString
except Exception as x:
    print(f"FATAL ERROR: We could not load all required libary's! -> {x}")
    os._exit(1)
    
class NFC_UID:
    __version = "0.5"
    __name="nfc-uid"
    pypi_version="0.5"
    logging = True
    last_chip = ""
    loop = True

    def __init__(self, logging=True):
        self.logging=logging
        if self.__is_pypi_version_newer() and self.logging:
            if self.pypi_version!=None:
                print(f"Update is available! You have [{self.__version}] but should have [{self.pypi_version}]")
            else:
                print("Update is available")
    def __is_pypi_version_newer(self):
        try:
            response = requests.get(f"https://pypi.org/pypi/{self.__name}/json")
            response.raise_for_status()
            data = response.json()
            latest_version = data["info"]["version"]
            self.pypi_version = latest_version
            return parse_version(latest_version) > parse_version(self.__version)
        except (requests.RequestException, KeyError):
            return False

    def _wait_for_card_removal(self, current_uid, connectTimeout=1, cooldown=0.2):
        """
        Blocks until the current card is removed.
        A different UID is treated as a new presentation and released for the next loop.
        """
        while self.loop:
            try:
                getuid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                act = AnyCardType()
                cr = CardRequest(timeout=connectTimeout, cardType=act)
                cs = cr.waitforcard()
                cs.connection.connect()
                data, sw1, sw2 = cs.connection.transmit(getuid)
                data = toHexString(data).replace(" ", "")

                if data != current_uid:
                    self.last_chip = ""
                    return

                time.sleep(cooldown)
            except CardRequestTimeoutException:
                self.last_chip = ""
                return
            except Exception as x:
                if self.logging:
                    print(f"Error while waiting for card removal: {x}")
                time.sleep(cooldown)

    def read(self, output=True, keyboardType=False, connectTimeout=120, maxRetrys=8, cooldown=2):
        """
        Returns UID of NFC Chip/Card
        Set ouput to False if no print/output is required default is True
        output -> def = True               | Output for success/feedback etc. will be enabled
        connectTimeout -> def = 120/2min   | Sets timeout in seconds. Timeout for scan card.
        maxRetrys -> def 8                 | Sets maximum read trys befor break. Set to None for infinite
        retryCooldown -> def 2             | Sets timeout in seconds for read retry
        """
        counter = 0
        while maxRetrys==None or counter<maxRetrys:
            try:
                if output:
                    print("Waiting for NFC-Card..")
                getuid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                act = AnyCardType()
                cr = CardRequest(timeout=connectTimeout, cardType=act)
                cs = cr.waitforcard()
                cs.connection.connect()
                data, sw1, sw2 = cs.connection.transmit(getuid)
                data = toHexString(data)
                data = data.replace(" ", "")
                if data and (not keyboardType or data != self.last_chip):
                    self.last_chip = data
                    if output:
                        print(f"Success in reading chip..\nUID: {data}")
                    if keyboardType:
                        if self.logging:
                            print("Output send to keyboard")
                        Keyboard.write(f"{data}")
                    else:
                        return data
                    return data
                cs = None
            except CardRequestTimeoutException:
                if keyboardType:
                    self.last_chip = ""
                if self.logging:
                    print("Connection timed out... New request starting")
            except Exception as x:
                if self.logging:
                    print(f"Error: {x}")
            counter+=1
            time.sleep(cooldown)

    def nfc_reader(self, debug=True ,output=True, keyboard_output=False, set_timeout=120, set_cooldown = 3):
        """
        Returns UID of NFC Chip/Card
        Set ouput to False if no output is required default is True
        debug -> def = True          | Output for errors etc. will be enabled
        output -> def = True         | Output for success/feedback etc. will be enabled
        keyboard_output -> def False | Types output like typing it
        set_timeout -> def 120/2min  | Sets timeout in seconds. Timeout for scan card.
        """
        if self.logging:
            print("Function nfc_read is depricated! Please change to read")

        while True:
            try:
                if output:
                    print("Waiting for Card..")
                getuid=[0xFF, 0xCA, 0x00, 0x00, 0x00]
                act = AnyCardType()
                cr = CardRequest( timeout=set_timeout, cardType=act )
                cs = cr.waitforcard()
                cs.connection.connect()
                data, sw1, sw2 = cs.connection.transmit(getuid)
                data = toHexString(data)
                data = data.replace(" ", "")
                if data and (not keyboard_output or data != self.last_chip):
                    self.last_chip = data
                    if output:
                        print(f"Success in reading chip..\nUID: {data}")
                    if keyboard_output:
                        if debug:
                            print("Output send to keyboard")
                        Keyboard.write(f"{data}")
                    else:
                        return data
                    time.sleep(set_cooldown)
                    return data
                cs=None
            except CardRequestTimeoutException:
                if keyboard_output:
                    self.last_chip = ""
                if debug:
                    print("Connection timed out... New request starting")
            except Exception as x:
                if debug:
                    print(f"Error: {x}")

    def looped_read(self, output=True, keyboardType=False, connectTimeout=120, maxRetrys=8, cooldown=2):
        """
        While loop for NFC_UID.read
        Will be looped until Enviroment.__loop__ is False
        USE WITH THREAD ONLY!
        output -> def = True               | Output for success/feedback etc. will be enabled
        connectTimeout -> def = 120/2min   | Sets timeout in seconds. Timeout for scan card.
        maxRetrys -> def 8                 | Sets maximum read trys befor break. Set to None for infinite
        retryCooldown -> def 2             | Sets timeout in seconds for read retry
        """
        while self.loop:
            data = self.read(
                output=output,
                keyboardType=keyboardType,
                connectTimeout=connectTimeout,
                maxRetrys=maxRetrys,
                cooldown=cooldown,
            )
            if keyboardType and data:
                self._wait_for_card_removal(data)

if __name__ == "__main__":
    reader = NFC_UID()
    reader.read()
