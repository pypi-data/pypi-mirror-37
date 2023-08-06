import sys, socket
from optparse import OptionParser
from . import stock_notifier

def _getpid():
    try:
        pf = file(stock_notifier.StockNotifier.PIDFILE,'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None
    return pid

def _start():
    pid = _getpid()
    if pid:
        sys.stdout.write("Process already running with pid: %s" % pid)
    else:
        stckNtfr = stock_notifier.StockNotifier()
        stckNtfr.start()

def _add(options):
    msg = "ADD " + options.add 
    _send_message(msg)

def _remove(options):
    msg = "REMOVE " + options.remove
    _send_message(msg)

def _send_message(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((stock_notifier.StockNotifier.LOCALHOST, stock_notifier.StockNotifier.PORT))
    sock.sendall(msg)
    sock.close()

def _parse_options():
    parser = OptionParser()
    parser.add_option("-s", "--start", dest="start", action="store_true",
                      help="start monitoring stocks")
    parser.add_option("-a", "--add", dest="add",
                      help="add stock to monitor")
    parser.add_option("-r", "--remove", dest="remove", 
                      help="remove stock which is being monitored")
    (options, args) = parser.parse_args()
    return options

def main():
    options = _parse_options()
    if options.start:
        _start()
    elif options.add:
        _add(options)
    elif options.remove:
        _remove(options)
