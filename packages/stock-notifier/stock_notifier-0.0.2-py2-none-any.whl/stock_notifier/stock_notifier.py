# -*- coding: utf-8 -*-
"""
This class manages the fetching of stock data and notifications.
"""

import pync
import os, sys, atexit, signal, socket
import time
from stock_config.nasdaq_stock_config import NasdaqStockConfig


class StockNotifier:
    
    PIDFILE = "/tmp/stocknotifier.pid"
    LOCALHOST = '127.0.0.1'
    PORT = 8888
    
    def __init__(self, pidfile = PIDFILE, stock_symbols=[], stdin='/dev/null', 
                 stdout='/dev/null', stderr='/dev/null'):
        self.stock_symbols = stock_symbols
        self.pidfile = pidfile
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((StockNotifier.LOCALHOST, StockNotifier.PORT))
        self.sock.setblocking(0)
        self.sock.listen(1)
        self.message_to_action_map = {
                "TEST" : self.test_message_action,
                "ADD": self.add_stock_action,
                "REMOVE": self.remove_stock_action
        }
        
    def test_message_action(self, data):
        """
        Tests communication between process and handler
        """
        pync.notify(data[1])
    
    def add_stock_action(self, data):
        """
        Action which adds a stock symbol to monitor
        """
        self._add_stock_symbol(data[1])
        
    def remove_stock_action(self, data):
        """
        Action which removes a stock symbol from the monitor
        """
        self._remove_stock_symbol(data[1])
    
    def _show_notification_message(self, stock):
        """
        Displays notification message to the screen.
        """
        _title = "%s Stock Notification" % (stock.get_stock_symbol().upper())
        _message = "Your stock value is %s. The stock has %s by %s." % \
            (stock.get_stock_value(), stock.get_stock_margin(), stock.get_stock_value_difference())
        pync.notify(_message, title = _title) 
    
    def _notify(self):
        """
        Fetches stock data and displays notifications based on configuration.
        """
        for stock_symbol in self.stock_symbols:
            stock = NasdaqStockConfig.get_stock_data(stock_symbol)
            self._show_notification_message(stock)
    
    def _add_stock_symbol(self, stock_symbol):
        """
        Adds stock symbol to the list of monitored stocks
        """
        if stock_symbol not in self.stock_symbols:
            self.stock_symbols.append(stock_symbol)
    
    def _remove_stock_symbol(self, stock_symbol):
        """
        Removes stock symbol from the list of monitored stocks
        """
        if stock_symbol in self.stock_symbols:
            self.stock_symbols.remove(stock_symbol)
    
    def _daemonize(self):
        """
        Creates a daemon process.
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit the first parent
                sys.exit(0)
        except OSError, e:
            print("#1 Fork failed: %d (%s)\n" %(e.errno, e.strerror))
            sys.exit(1)
        
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit the first parent
                sys.exit(0)
        except OSError, e:
            print("#2 Fork failed: %d (%s)\n" %(e.errno, e.strerror))
            sys.exit(1)
            
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
        #write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
        
    
    def delpid(self):
        """
        Removes the pid file created for the process.
        """
        os.remove(self.pidfile)
    
    def start(self):
        """
        Starts the daemon
        """
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
            
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            print(message % self.pidfile)
            sys.exit(1)
        
        self._daemonize()
        self.run()
        
    def run(self):
        """
        Method which is run as a daemon
        """
        while True:
            try:
                conn, addr = self.sock.accept()
                message = conn.recv(1000)
                data = message.split(" ")
                if message:
                    self.message_to_action_map[data[0]](data)
            except socket.error:
                pass
            self._notify()
            time.sleep(15)
    
    def stop(self):
        """
        Method to stop the daemon process.
        """
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
            
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return
        
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
                
    def restart(self):
        """
        Restarts the daemon process
        """
        self.stop()
        self.start()
        
    def get_pid(self):
        """
        Returns the process id of the process.
        """
        return self.pidfile
