import nfc
import nfc.ndef
import ndef

def connected(tag):
    print "format: ", tag.format()
    print "on card: ", tag.ndef.message.pretty() if tag.ndef else "sorry no NDEF"
    for record in tag.ndef.records:
        print(record)
    # uri, title = 'sonos:line-in', 'Living Room'
    uri, title = 'sonos:radio', 'aac://http://live-aacplus-64.kexp.org/kexp64.aac'
    tag.ndef.records = [ndef.SmartposterRecord(uri, title)]
    return False

if __name__ == "__main__":
    with nfc.ContactlessFrontend("tty:S0:pn532") as clf:
        print clf
        clf.connect(rdwr={"on-connect": connected})

