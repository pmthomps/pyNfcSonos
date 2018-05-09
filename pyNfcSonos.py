import nfc
import soco
import nfc.ndef
import ndef

# Constants
NFC_SONOS = "Living Room"
NFC_CONN = "tty:S0:pn532"
 
def tagConnected(tag): 
    print "Tag read!"
    print tag 

    record = nfc.ndef.SmartPosterRecord(tag.ndef.message[0])
    
    # validate tag
    validateTag(record)

    tagInstruction = getInstruction(record)

	# connect to sonos
    sonosDevice = getSonos()

    # tell it go play Living Room line-in
    if tagInstruction['type'] == "line-in": 
        print "Received tag instruction for line-in to: " + tagInstruction['resource']
        sonosDevice.switch_to_line_in(getSonosLineIn(tagInstruction['resource']))
        sonosDevice.play()
    elif tagInstruction['type'] == "radio": 
        print "Received tag instruction for radio to: " + tagInstruction['resource']
        sonosDevice.play_uri(uri=tagInstruction['resource'], start=True, force_radio=True)
    else:
        print "Unknown tag instruction: " +  tagInstruction['type']

    return False	

def getSonos(): 
    nfcSonos = soco.discovery.by_name(NFC_SONOS)
    sonosCoordinator = nfcSonos.group.coordinator
	
    print "Got sonos coordinator: " + sonosCoordinator.player_name

    return sonosCoordinator
 
def getSonosLineIn(instance_name): 
    sonosTt = soco.discovery.by_name(instance_name)

    print "Got sonos turntable: " + sonosTt.player_name
    return sonosTt

def validateTag(record):
    print record
    # slice on scheme and check it == "sonos"

    return True

def getInstruction(record): 
    # slice on the authority (sonos:) (position 57 to end) 
    print "URI Authority: " + record.uri[6:]
    print "title: " + record.title['en']

    instruction = dict()
    instruction['type'] = record.uri[6:]
    instruction['resource'] = record.title['en']

    return instruction

def main(): 
    # while True
        with nfc.ContactlessFrontend(NFC_CONN) as nfcReader: 
            print "NFCReader connected!"
            print nfcReader

            print "Waiting for tag..."
            nfcReader.connect(rdwr={"on-connect": tagConnected})

if __name__ == "__main__": 
    main()
