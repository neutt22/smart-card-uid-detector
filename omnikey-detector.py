from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *
import sys
from smartcard.scard import *
import webbrowser


class PrintObserver(CardObserver):
    def update(self, observable, (addedcards, removedcards)):
        for card in addedcards:
            print "+Inserted: ", toHexString(card.atr)

            hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            assert hresult == SCARD_S_SUCCESS
            hresult, readers = SCardListReaders(hcontext, [])
            assert len(readers) > 0
            reader = readers[0]
            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext,
                reader,
                SCARD_SHARE_SHARED,
                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
            hresult, response = SCardTransmit(hcard, dwActiveProtocol, [0xFF, 0xCA, 0x00, 0x00, 0x00])
            webbrowser.open('http://foo.bar/?uid=' + ''.join(str(e) for e in response))
        for card in removedcards:
            print "-Removed:  ", toHexString(card.atr)

try:
    print "Insert or remove a smartcard in the system."
    print ""
    cardmonitor = CardMonitor()
    cardobserver = PrintObserver()
    cardmonitor.addObserver(cardobserver)
    raw_input('Press Enter to exit\n')
except:
    print "Unexpected error: ", sys.exc_info()[0]
