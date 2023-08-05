# -*- coding: utf-8 -*-
"""
Copyright © 2017-2018 The University of New South Wales

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name or trademarks of a copyright holder

shall not be used in advertising or otherwise to promote the sale, use or other
dealings in this Software without prior written authorization of the copyright
holder.

UNSW is a trademark of The University of New South Wales.


:date: Thu Jul 27 20:40:36 2017
:author: kjetil


This module contains utility functions such as Exception handling for the
libgs library

"""
from __future__ import print_function

import threading

import logging
import time
import os
import pandas as pd
import traceback
import collections
from datetime import datetime
import ephem
from libgs_ops.rpc import RPCClient


abort_all = threading.Event()

log = logging.getLogger('libgs-log')
log.addHandler(logging.NullHandler())



##########################
#
# Exceptions
#
##########################

class Error(Exception):
    """Generic Error for this module"""

    def __init__(self, msg, original_Error=None):
        if original_Error is not None:
            super(Error, self).__init__(msg + (": %s" % original_Error))
            self.original_Error = original_Error
        else:
            super(Error, self).__init__(msg)


class AbortAllException(Error):
    """
    Exception representing the abort_all event
    """
    pass


##########################
#
# Default values used throughout
#
##########################


class Defaults:
    """
    Defines default values used by the different
    classes
    """

    #
    # The interval at which to save monitoring values to database
    # when tracking and when not tracking
    #
    MONITOR_SAVE_DT_TRACK   = 5   # 5 seconds
    MONITOR_SAVE_DT_NOTRACK = 900 # 15 minutes


    ##############################################
    #
    # Hardware interfaces
    #
    ##############################################

    #
    # XMLRPC interface to scheduler
    #
    XMLRPC_SCH_SERVER_ADDR = "localhost"
    XMLRPC_SCH_SERVER_PORT = 8000

    #
    # XMLRPC interface to ground station
    #
    XMLRPC_GS_SERVER_ADDR = "localhost"
    XMLRPC_GS_SERVER_PORT = 8001

    #
    # Default client timeout
    #
    XMLRPC_CLI_TIMEOUT = 2
    


    #
    # Dashboard port
    #
    DASH_PORT = 5001

    #
    # REST API
    #
    API_ADDR = "localhost"
    API_PORT = 8080



    ##############################################
    #
    # Configuration parameters
    #
    ##############################################


    #
    # Default rotator configurations
    # (Set in rotator base class, but usually overwritten in derived classes)
    #
    ROTATOR_STOWED_AZ = 0
    ROTATOR_STOWED_EL = 90
    ROTATOR_ANTENNA_BEAMWIDTH = 10 #<-- sets the granularity at which the rotator moves the antenna
    ROTATOR_MAX_AZ    = 360
    ROTATOR_MIN_AZ    = 0
    ROTATOR_MAX_EL    = 90
    ROTATOR_MIN_EL    = 0
    ROTATOR_SLEW_TIMEOUT = 100


    #
    # Log config
    #
    LOG_PATH = './logs'       # path to store files in
    LOG_FILE = 'libgs.log'    # log file name
    LOG_BACKUPCOUNT = 100     # number of files to keep
    LOG_MAXFILESIZE = 1000000 # Max filesize in bytes
    LOG_FORMAT = '%(asctime)s - %(name)14s - %(levelname)5s - %(module)20s:%(lineno)4s - "%(message)s"'
    LOG_STRING_LEN = 23+3+14+3+5+3 + 24+3+1

    #
    # Length of log to keep in UI
    #
    UI_LOG_LEN = 20



    #
    # Database connection (See SQLAlchemy for syntax)
    #
    DB = 'sqlite:///libgs.db'


    #
    # Rotctld ppolling
    # TODO: This might also be an old one that should be removed
    #
    GS_ROTATOR_POLLING_INTERVAL = 0.25



    #
    # Communications timeout after requesting data, and waiting for reply
    #
    TX_REPLY_TIMEOUT=1000 #<--- large number to let spacelink handle the timeouts.


    #
    # Color log entries
    #
    USE_LOG_COLOUR = True

    #
    # Log level  for extra verbose logging (normally disabled but can be enabled)
    #
    # VERY_VERB_LOG = 5

    #
    # Schedule defaults
    #
    # SCHEDULE_BUFFERTIME = 180


    #
    # Update delay for frequency plot (should be around .2 - 2)
    #
    VIS_FREQUENCY_PLOT_UPDATE_DELAY = .5


    #
    # Spectrum recording
    #
    RECORD_SPECTRA = True
    RECORD_SPECTRA_MAX_LEN = 900
    RECORD_SPECTRA_DT = 1.0
    

    #
    # Path to store datafiles in (that are not stored in db)
    #
    DB_BIN_PATH = '.'
    DATA_PATH = DB_BIN_PATH #<-- todo: refactor and delete

    #
    # Visualisation waterfalls
    #
    WFALL_COLORMAP = 'Viridis256' #<--- Bokeh colormap. see https://bokeh.pydata.org/en/0.12.6/docs/reference/palettes.html
    WFALL_JPG_COLORMAP = 'viridis' #<-- Matplotlib colormap. See: https://matplotlib.org/examples/color/colormaps_reference.html
    WFALL_JPG_WIDTH = 250 #<--- width per plot (in pixels) if dpi=100
    WFALL_JPG_HEIGHT = 600 #<--- height of pllot (in pixels) if dpi = 100
    WFALL_JPG_WIDTH_EXTRA = 200 #<--- extra width (in addition to plots) in pixels if dpi = 100
    WFALL_JPG_DPI = 100
    WFALL_JPG_OUT_SCALE = 1 #<-- scale dpi on output . Affects font size

    #
    # REST API
    #
    RESTAPI_DEBUG_MODE = False #<-- put restapi in debug mode (more verbose error messages)
    RESTAPI_TABLE_LIMIT = 400  #<-- max rows to return by restapi if nothing has been explicitly given

########################
#
# Functions and classes
#
########################

def raise_if_aborted():
    """
    This method will raise an exception if the abort_all global event has been set.
    """
    if abort_all.is_set():
        raise AbortAllException("abort_all event has been set")



class RegularCallback(object):

    def __init__(self, func, delay, min_interval=0.05):
        """

        Args:
            func:  Callback funciton to call
            delay: Time between two subsequent calls
            min_interval: Minimum time between the end of one call and the beginning of th next

        """
        self.func = func
        self.delay = delay
        self._pthr = threading.Thread(target=self._regular_callback)
        self._pthr.daemon = True
        self.min_interval=min_interval
        self._suppressing_errors = False
        self._last_e = (None, None)

    def _regular_callback(self):
        """
            A function to regularly call a callback based on the specified delay
        """

        # This property can be changed to stop the callback
        self._stop_thread = False
        stop_thread_fn = lambda: self._stop_thread
        
        log.debug("Regular callback of '{}' started".format(self.func.__name__))

        while True:

            t0 = time.time()

            try:
                self.func()
            except Exception, e:
                new_e = (e.__class__.__name__, str(e))
                if new_e == self._last_e:
                    if not self._suppressing_errors:
                        log.error("Repeat Exception '{}:{}' in regular callback, suppressing output until something new happens".format(*new_e))
                        self._suppressing_errors = True

                else:
                    if self._suppressing_errors:
                        log.info("Repeat Exception '{}:{}' has stopped occurring. Regular callback resumed normal operation".format(*self._last_e))
                    self._suppressing_errors = False
                    self._last_e = new_e
                    err = traceback.format_exc()
                    log.error("Exception in regular callback function. Stack trace:\n%s"%(err))
                #Error("Exception in regular callback function: %s"%(e))

            # Sleep until next call unless an event happens in which case we break from the loop
            try:
                if wait_loop([stop_thread_fn], timeout=max(self.delay - (time.time() - t0), self.min_interval)) is not None:
                    break
            except AbortAllException as e:
                log.debug("Abort All event caught. Shutting down regular callback")
                break


        log.debug("Regular callback of '{}' ended".format(self.func.__name__))
            #time.sleep(max(self.delay - (time.time() - t0), self.min_interval))

    def start(self):
        self._pthr.start()

    def stop(self):
        self._stop_thread = True
        self._pthr.join()



def conv_time(d, to='iso', float_t='julian', ignore_ambig_types = False):
    """
    There are a number of different date formats used around libgs
    ephem.Date, datetime, pandas.Timestamp to mention some.
    Also modified Julian time and various string formats.
    
    
    """
    if ignore_ambig_types and not (isinstance(d, ephem.Date) or isinstance(d, pd.Timestamp) or isinstance(d, datetime)):
        return d
        
    
    # first make a pandas Timestamp object
    if isinstance(d, ephem.Date):
        d2 = pd.to_datetime(d.datetime())
    elif isinstance(d, pd.Timestamp):
        d2 = d
    elif isinstance(d, float):
        if float_t == 'julian':
            d2 = pd.to_datetime(d, unit='D', origin='julian')
        elif float_t == 'unix':
            d2 = pd.to_datetime(d, unit="s", origin="unix" )
            #d2 = pd.to_datetime(datetime.fromtimestamp(d))
        else:
            raise Error("Unknown float  time type {}".format(float_t))
    elif isinstance(d, basestring):
        # Try to work out if we have year first (iso like or day first)
        if len(d.split('-')[0].strip()) == 4:
            d2 = pd.to_datetime(d)
        else:
            d2 = pd.to_datetime(d, dayfirst=True)
    elif isinstance(d, datetime):
        d2 = pd.to_datetime(d)
    else:
        raise Error("Dont know how to convert obejct of type {} to time".format(type(d)))

    d2 = d2.replace(tzinfo=None)

    if to == 'iso': #w milliseconds
        d3 = d2.strftime('%Y-%m-%dT%H:%M:%S,%f')[:-3]   
        d3 += 'Z'
    elif to == 'julian':
        d3 =d2.replace(tzinfo=None).to_julian_date()
    elif to == 'unix':
        d3= time.mktime(d2.timetuple()) + d2.microsecond/1e6
    elif to == 'datetime':
        d3 = d2.to_pydatetime()
    elif to == 'pandas':
        d3 = d2
    elif to == 'ephem':
        d3 = ephem.Date(d2.to_pydatetime())
    else:
        raise Error("Dont know how to convert to {}".format(to))
        
        
    return d3


def wait_loop(events_or_callables = [], timeout=None, dt=0.1):
    """
    Generic waiting loop. It will wait for any event
    (of type threading.Event) to be set, or for any callable to return True
    """
    t0 = time.time()

    if not isinstance(events_or_callables, collections.Iterable):
        events_or_callables = [events_or_callables]

    fns = [ec.is_set if isinstance(ec, threading._Event) else ec for ec in events_or_callables]

    for ec in events_or_callables:
        if not (isinstance(ec, threading._Event) or callable(ec)):
            raise Error("events_or_callable must be a list of events or callables, got {}".format(type(ec)))


    while True:

        if abort_all.is_set():
            raise AbortAllException("global wait_loop abort_all has been set")

        if timeout is not None and time.time() - t0 > timeout:
            return None


        e_set = [e for (e,f) in zip(events_or_callables, fns) if f()]

        if len(e_set) > 0:
            return e_set


        rdt = max(0, timeout - (time.time() - t0)) if timeout is not None else 0
        time.sleep(min(rdt, dt))


def safe_sleep(t):
    """
    safe_sleep uses a subset of the wait_loop capabilities to implement an anologe to the time.sleep() function.

    The advantage is that it will raise an exception if the global abort event gets set, and as such is safe to
    use in thread loops that need to exit on adfa-gs exit.

    """
    wait_loop(timeout=t)


class Monitor(object):
    """
    Basic class to monitor //anything//. Mainly used for
    ground station telemetry points. Can classify points as
    RED/ORANGE/GREEN and give alerts if something is out of range.
    """

    _alert_codes = dict(
         CRITICAL =  100,
         RED      =  30,
         ORANGE   =  20,
         GREEN    =  10,
         NO_ALERT =  0)

    NO_PASS = 'no pass'

    def __init__(self, dt = 2.0, dtdb = 10.0, db = None):
        """
        Args:
           dt   (float)  : The interval (in s) at which to run the poller
                           Variables can only be polled at an integer multiple of dt (see register_monitor)
           dtdb (float)  : The interval (in s) at which to store the monitored values in the db
           db            : The SQLAlchemy connection for the db to store values to
        """

        self._dt = dt #<-- minimum unit of time for regular callback

        self._exec_map = pd.DataFrame(columns=['exec_t', 'name', 'parent', 'rate', 'fn', 'alert_fn', 'loglvl', 'logalerts', 'value', 'alert', 'fn_error', 'alert_fn_error', 'last_db_t'])
        self._parents = {}

        if db is None:
            log.info("No db specified for logging monitor values")
            self._db = None
        else:
            self.db = db

        self.dtdb = dtdb #<-- minimum time between each time data is stored in database")

        # must be updated by GS
        self.pass_id = self.NO_PASS

        # A callback that can be set or not. Whenever the monitor updates
        # the callback will be called with a reference to the monitor
        self.callback = None
        
        # Register private monitor points
        self._internal = dict(
            runcount = 0,
            runtime  = 0,
            runtime_acc = 0,
            num_polled = 0,
            num_polled_acc = 0)
        #self.register_parent('_internal')
        # Monitor execution time. Set update rate to -1 as it is updated
        # from the _handle_callback method
        # TODO: Decide if this type of custom entry in exec_map is really
        # the best or if we should deal with this one a bit differently...
#        self._exec_map = self._exec_map.append(dict(
#            exec_t = time.time(),
#            name = '_runtime',
#            rate = 1e12,
#            fn = lambda: 0,
#            parent = '_internal',
#            alert_fn = None,
#            logalerts = None,
#            logvalues = None,
#            value = None,
#            alert = None),
#            ignore_index=True)        
#        


    def start(self):
        self._regcb = RegularCallback(
            func=self._handle_callback,
            delay=self._dt,
            min_interval=1.0)
        self._regcb.start()


    def stop(self):
        self._regcb.stop()
        del(self._regcb)

    @property
    def dtdb(self):
        return self._dtdb

    @dtdb.setter
    def dtdb(self, val):
        if not (isinstance(val, int) or isinstance(val, float)):
            raise Error("Invalid type for dtdb, got {}".format(type(val)))

        if val < self._dt:
            raise Error("dtdb must be > dt({}). You tried to set it to {}".format(self._dt, val))

        self._dtdb = val

    @property
    def db(self):
        return self._db
        
    @db.setter
    def db(self, val):
        #TODO: type checking (not possible while Monitor is in utils module as we cant import databases.py)
        self._db = val


    @property
    def state(self):
        if len(self._exec_map[self._exec_map.alert == 'RED']) > 0:
            return 'RED'
        else:
            return 'GREEN'


    def _check_alert(self, val):
        if val not in self._alert_codes.keys():
            log.error("Invalid alert '{}', setting it to RED. Must be one of {}".format(val, self._alert_codes))
            val = 'RED'

        return val


    def _set_value(self, k, val, alert=None):
        #self._exec_map.set_value(k, 'value', val)#loc[k, ['value']] = [val]
        self._exec_map.at[k, 'value'] = val
        
        if not alert is None:
            self._exec_map.loc[k, 'alert'] = self._check_alert(alert)

        # Add values to log if threshold for how often to do so has been
        # exceeded
        if self._db is not None:
            t = time.time()
            if pd.isnull(self._exec_map.loc[k, 'last_db_t']) or \
               (t - self._exec_map.loc[k, 'last_db_t']) > self.dtdb:
                self._db.put(pass_id= self.pass_id,
                             key = self._exec_map.loc[k, 'name'],
                             value = val,
                             alert=alert)
                self._exec_map.loc[k, 'last_db_t'] = t


    # TODO: Add stats about _internal to the monitor properly
#    def _internal_stats(self, k):
#        last =  self._internal_stats_last
#        ret = dict(
#            runcount = self._internal['runcount'],
#            num_polled_acc = self._internal['num_polled_acc'],
#            num_polled_avg = (self._internal['num_polled_acc'] - last['num_polled_acc'] )/(self._internal['runcount'] - last['runcount'])
#            )
#        return ret

    def _handle_callback(self):
        """
        Handle callback depending on the set schedule.
        """
        self._exec_map.sort_values('exec_t', inplace=True)


        #
        # Get the variables that are due for polling and loop through them
        # to poll.
        #
        to_exec = self._exec_map[time.time() > self._exec_map.exec_t]

        t0 = time.time()
        polled_count = 0
        for k, item in to_exec.iterrows():

            self._exec_map.loc[k, 'exec_t'] += self._exec_map.loc[k, 'rate']

            try:
                val = item['fn']()
                polled_count += 1
                self._exec_map.loc[k, 'fn_error'] = None
            except Exception, e:

                if item['alert_fn'] is not None:
                    self._set_value(k, "ERROR", "RED")
                else:
                    self._set_value(k, "ERROR")

                if pd.isnull(item['fn_error']):
                    log.debug("{} reading monitor value {}: {}".format(e.__class__.__name__, item['name'], e))
                    self._exec_map.loc[k, 'fn_error'] = e

                return


            #
            # Log a change in value if requested and as requested
            #
            if (self._exec_map.loc[k, 'value'] != val) and (item['logvalues'] is not None):
                log.log(int(item['logvalues']), 'Monitor: value "{}" --> {}'.format(item['name'], val))

            #
            # Log a change in alert if requested and as requested
            #
            new_alert = None
            if item['alert_fn'] is not None:
                old_alert = self._exec_map.loc[k, 'alert']


                try:
                    new_alert = item['alert_fn'](val)
                    self._exec_map.loc[k, 'alert_fn_error'] = None
                except Exception, e:
                    new_alert = 'RED'

                    if pd.isnull(item['alert_fn_error']):# is None:
                        log.error("Exception reading monitor alert function {}: {}".format(item['alert_fn'], e))
                        self._exec_map.loc[k, 'alert_fn_error'] = e

                new_alert = self._check_alert(new_alert)

                #print("BLAH", item)
#                if old_alert != new_alert and new_alert in item['logalerts'].keys():
#                    log.log(int(item['logalerts'][new_alert]), 'Monitor: ALERT "%s" --> %s (%s)'%(item['name'], new_alert, val))




            #
            # Update monitored variable
            #
            self._set_value(k, val, new_alert)
            
            
#        # Store the time it took to monitor everything
#        # TODO: If the time is too long, take some sort
#        # of preventative action
#        dt = time.time() - t0
#        k = self._exec_map.index[self._exec_map.name == '_runtime'][0]
#        #self._exec_map.loc[k, 'exec_t'] += self._exec_map.loc[k, 'rate']
#        self._set_value(k, dt)
            
        self._internal['runcount'] += 1
        self._internal['runtime'] = time.time() - t0
        self._internal['runtime_acc'] += self._internal['runtime']
        self._internal['num_polled'] = polled_count
        self._internal['num_polled_acc'] += polled_count

        #
        # Callback
        #
        if self.callback is not None:
            
            # This callback, if set, wll just return the monitor itself
            # as well as the time it took it to run.
            try:
                self.callback(self)
            except Exception as e:
                log.error("Error calling callback from Monitor: {}:{}".format(e.__class__.__name__, e))


    def __str__(self):
        t0 = time.time()


        # Recursive function to print all monitor points under their respective parents
        def print_parent(parent = None, prefix=''):

                if parent is None:
                    idx = pd.isnull(self._exec_map.parent)
                else:
                    idx = self._exec_map.parent == parent

                ret =  self._exec_map.loc[idx, ['name', 'value', 'alert', 'exec_t', 'rate', 'parent']].sort_values('name').set_index('name')

                headers = list(ret.index) + [k for k,p in self._parents.items() if p['parent'] == parent]
                headers.sort()

                maxalert = None

                s = ""
                for header in headers:
                    if header in ret.index:
                        v = ret.loc[header,:]
                        
                        s += "{:30.29s}{:20.19s}{:10.19s}{:15s}\n".format(
                            prefix +v.name,
                            str(v.value),
                            v.alert,
                            '{:<15.1f}'.format(t0 - (v.exec_t - v.rate)) if hasattr(self, '_regcb') else 'not running')

                        alert = v.alert
                           
                    elif header in self._parents.keys():
                        s2, alert = print_parent( parent = header, prefix = prefix+'.')
                        s += "{:30.29s}{:20.19s}{:10.19s}{:15s}\n".format(prefix + header, '', alert, '')
                            
                        s += s2

                    if alert is not None:
                        if maxalert is None or self._alert_codes[alert] > maxalert:
                            maxalert = alert


                return s, maxalert

        s2, alert =  print_parent()

        s  =  "Monitor ({})\n".format(alert)
        s += "%-30s%-20s%-10s%-15s\n"%("Name", "Value", "Alert", "Last polled")
        s +=  "-"*29+ " " +"-"*19+" "+ "-"*9 + " " + "-"*15 + "\n"
        
        #
        # First add internals (these are not in exec_map)
        #
        s += "{:30.29s}{:20.19s}{:10.19s}{:15s}\n".format('_internal', '', '', '')
        for k,v in self._internal.items():
            s += "{:30.29s}{:20.19s}{:10.19s}{:15s}\n".format('._'+k, str(v), '', '')

        #
        # Then print the rest
        #
        s += s2


        return s


    def __repr__(self):
        return self.__str__()


    def register_parent(self,
                        name,
                        parent = None):
        """
        A parent monitor is not really a monitor. It is merely the product
        of its children and exists for visualisation purposes only.

        Its alert status will always be the worst of its children

        """

        self._parents[name] = dict(parent=parent)#, log_values=log_values, log_alerts = log_alerts)
#        self._exec_map = self._exec_map.append(dict(
#            name = name,
#            parent = parent,
#            logalerts = log_alerts,
#            logvalues = log_values),
#            ignore_index=True)



    def rebalance_polling(self):
        """
        Reset execution times so that polling is relatively evenly split
        across polling cycles.
        """
        
        cntr = 0
        t0 = time.time()
        for k,v in self._exec_map.iterrows():
            self._exec_map.loc[k, 'exec_t'] = t0 + self._exec_map.loc[k, 'rate'] +  cntr % self._exec_map.loc[k, 'rate']
            cntr += self._dt
            
        

    # TODO: Make it possible to register a function that returns several values
    def register_monitor(self,
                         name,
                         rate,
                         fn,
                         parent = None,
                         alert_fn=None,
                         log_values = logging.DEBUG,
                         log_alerts=['CRITICAL', 'RED', 'GREEN', 'ORANGE']):
        """
        A monitor is defined by:
          * a function that will poll for a value,
          * a rate at which the polling will happen (should ideally be a
            multiple of dt, otherwise it will be rounded to the upper of the nearest
            multiple of dt)
          * an alert processor funcion. Set to None to disable alerting.

         Args:
             name (string)   : The name of the monitor point
             rate (float)    : The delay (in s) between each poll
             fn   (function) : The function to call when polling
             parent (str)    : A parent monitor. The parents alert will always be the worst of its children
             alert_fn (func) : The function to call to get alert level (if appl)
             log_alert (list): Display state change in log when alert changes
                               to one of these levels. Can be empty list or any
                               combination of 'RED', 'GREEN', 'ORANGE'.
                               Can also be a dict where the value is the logging level.
                               Default: ['CRITICAL', 'RED', 'GREEN', 'ORANGE'] and default
                               level is logging.INFO for GREEN/ORGANGE, and logging.ERROR
                               for RED and CRITICAL.
             log_values (int) : The level to which to log changes in values to
                                Set to None for no logging. Default: logging.DEBUG
        """

        # Allow to effectively disable updates by setting the rate to <= 0
        # Implemented by changing it to a very large number
        if rate <= 0:
            rate =  1e9

        if isinstance(log_alerts, list):
            keys = log_alerts
            log_alerts = dict()
            for k in keys:
                if k == 'RED' or k == 'CRITICAL':
                    log_alerts[k] = logging.ERROR
                else:
                    log_alerts[k] = logging.INFO

        elif not isinstance(log_alerts, dict):
            raise Error("log_alerts should be list or dict, got %s"%(type(log_alerts)))


        if parent is not None and parent not in self._parents.keys():
            raise Error("{} is not a valid parent. Create the parent by calling register_parent first".format(parent))

        if name in self._exec_map['name']:
            raise Error("{} already exists. Names must be unique".format(name))

        try:
            val = fn()
        except Exception as e:
            raise Error("monitor call function {} is not valid: {}".format(fn, e))

        if alert_fn is not None:
            try:
                self._check_alert(alert_fn(val))
            except Exception as e:
                raise Error("alert call function is not valid: {}".format(e))

        self._exec_map = self._exec_map.append(dict(
            exec_t = time.time(),
            name = name,
            rate = rate,
            fn = fn,
            parent = parent,
            alert_fn = alert_fn,
            logalerts = log_alerts,
            logvalues = log_values,
            value = None,
            alert = None),
            ignore_index=True)
        
        # Make sure value is of dtype=object so it can
        # accept values of different types
        if self._exec_map.value.dtype != 'object':
            self._exec_map.value = self._exec_map.value.astype('object')

        log.debug("Registered monitor '%s'"%(name))# at rate '%d'. fn=%s, alert_fn=%s')

        self._exec_map.sort_values('exec_t', inplace=True)



class UTCLogFormatter(logging.Formatter):
    converter = time.gmtime
    use_colour = Defaults.USE_LOG_COLOUR

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
        s = "%s.%03dZ" % (t, record.msecs)

        return s

    def format(self, record):

        s =  super(UTCLogFormatter, self).format(record)

        if record.levelno >= logging.ERROR and self.use_colour:
            s = "\033[1;31m%s\033[1;0m"%(s)

        return s

class UTCLogFormatterHTML(UTCLogFormatter):

    def format(self, record):

        frec   =  super(UTCLogFormatter, self).format(record)

        if record.levelno >= logging.ERROR and self.use_colour:
            s = '<pre style="color:red;'
        else:
            s = '<pre style="'

        #s += 'max-width: 100%;overflow-x: auto;">{}</pre>\n'.format(frec)
        s += '">{}</pre>\n'.format(frec)
        return s


def setup_logger(logger,
                 cons_loglvl = logging.INFO,
                 file_logpath=None,
                 file_loglvl=logging.INFO,
                 fmt=Defaults.LOG_FORMAT):
    """
    Function to set up logging for libgs. Should only ever be called
    once.

    It sill set up logging to console and to file if requested.

    It will also make sure all logging is timestamped in UTC time
    following ISO 8601

    Args:
     logger: The log to setup
     cons_loglvl: log level for console logging,
     file_logpath: Path to log to if logging to file (None for no file logging),
     file_loglvl: log level for file log
     fmt: log formatting string
    """

    if hasattr(logger, '_has_been_setup'):
        raise Error("setup_logger can only be called once per logger")



    #
    # TODO: NOTE: When moving to a python module, this stuff should probably
    # be in the __init__ ...
    #

    #
    # Add custom log level
    #
    DEBUG_LEVELV_NUM = 9
    logging.addLevelName(DEBUG_LEVELV_NUM, "DBG_V")
    def debugv(self, message, *args, **kws):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DEBUG_LEVELV_NUM, message, args, **kws)
    logging.Logger.debugv = debugv

    # create logger
    logger.setLevel(logging.DEBUG)

    # create formatter

    # class MyFormatter(logging.Formatter):
    #     converter = time.gmtime
    #     use_colour = Defaults.USE_LOG_COLOUR
    #
    #     def formatTime(self, record, datefmt=None):
    #         ct = self.converter(record.created)
    #         t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
    #         s = "%s.%03dZ" % (t, record.msecs)
    #
    #         return s
    #
    #     def format(self, record):
    #
    #         s =  super(MyFormatter, self).format(record)
    #
    #         if record.levelno >= logging.ERROR and self.use_colour:
    #             s = "\033[1;31m%s\033[1;0m"%(s)
    #
    #         return s



    formatter = UTCLogFormatter(fmt)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(cons_loglvl)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


    #
    # Set up file logging as specificed
    #
    if file_logpath is not None:

        logpath = os.path.realpath(file_logpath)

        if not os.path.exists(logpath):
            os.mkdir(logpath)


        cf = logging.handlers.TimedRotatingFileHandler(logpath +'/' + Defaults.LOG_FILE,when='midnight',interval=1,backupCount=0,utc=True)
        cf.setFormatter(formatter)
        cf.setLevel(file_loglvl)

        logger.addHandler(cf)

        logger.info("File-logging enabled to %s"%(logpath))


    logger._has_been_setup = True


def schedule_regular_callback(func, delay):
    cb =  RegularCallback(func, delay)
    cb.start()
    return cb




def _print( *arg, **kwarg):
    """
        Function to print.

        This wrapper funciton is provided to allow for more easy redirection
        of output to other destinations (including Bokeh GUI, or files) if
        necessary.

        It should be used for information targeted at an interactive user, not
        for logging messages

    """

    print(*arg, **kwarg)




def bytes2prettyhex(data, whitespacelen= Defaults.LOG_STRING_LEN):

    #log.info(st)

    st = ''
    if data is not None:
        data_array = bytearray(data)
        datastr=["%02X"%(x) for x in data_array]
        N = range(0, len(datastr), 16)
        for n in N:
           st += '\n' + (' '*whitespacelen) + "{:06x}  ".format(n) + "-".join(datastr[0+n:16+n])

    return st

def bytes2hex(data):
    data =bytearray(data)
    return('-'.join(["%02X"%(x) for x in data]))


def hex2bytes(hexstr):
    data = hexstr.split('-')
    return bytearray(''.join([chr(int(x, 16)) for x in data]))



class XMLRPCTimeoutServerProxy(RPCClient):
    """
    An alias for RPCServer.
    TODO: Refactor so we can delete
    """
    pass
    # """
    # A re-implementation of the ServerProxy that enables timeouts
    # """
    #
    # class TimeoutTransport(xmlrpclib.Transport):
    #
    #     def __init__(self, timeout, use_datetime=0):
    #         self.timeout = timeout
    #         # xmlrpclib uses old-style classes so we cannot use super()
    #         xmlrpclib.Transport.__init__(self, use_datetime)
    #
    #     def make_connection(self, host):
    #         connection = xmlrpclib.Transport.make_connection(self, host)
    #         connection.timeout = self.timeout
    #         return connection
    #
    #
    # def __init__(self, uri, timeout=Defaults.XMLRPC_CLI_TIMEOUT, transport=None, encoding=None, verbose=0, allow_none=0, use_datetime=0):
    #     t = self.TimeoutTransport(timeout)
    #     xmlrpclib.ServerProxy.__init__(self, uri, t, encoding, verbose, allow_none, use_datetime)



if __name__ == '__main__':
    x = 2
    setup_logger(log, cons_loglvl=logging.DEBUG)
    #m = Monitor(dt = 1)
    #fn = lambda: x
    #alfn = lambda r: 'RED' if r < 0 else 'GREEN'
    #m.register_monitor('blah test', 5, fn, alert_fn = alfn)
    #m.start()
