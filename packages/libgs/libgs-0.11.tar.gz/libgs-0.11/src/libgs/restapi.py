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


Created on Mon Sep 18 09:22:40 2017

REST API interface
-------------------


This API currently only allows access to download data from the telemetry
database. It could be extended to provide more full control of the ground station
if necessary.

.. todo:: authentication

@author: kjetil
"""

from flask import Flask, current_app, request, g
from threading import Thread, Event
from utils import Defaults, hex2bytes, bytes2hex, conv_time
from database import TSTAMP_LBL
from pandas import to_datetime
from urllib import unquote
from utils import XMLRPCTimeoutServerProxy, wait_loop
import json
from base64 import b64encode, encodestring
import sys
import logging
ags_log = logging.getLogger('libgs-log')
ags_log.addHandler(logging.NullHandler())

app = Flask(__name__)
app.use_reloader = False


#
# DEBUG mode. Will show more explicit exceptions if enabled
#
DEBUG = Defaults.RESTAPI_DEBUG_MODE

#
# Limit returned table sizes by default to prevent overloading the processor
# trying to fetch an entire giant table. The user will  have to
# add N= specifically to request larger tables.
#
DEFAULT_TABLE_LIMIT = Defaults.RESTAPI_TABLE_LIMIT

#
# This  module allows the user to assign RPC apis to any endpoint
# In order to avoid conflict with the internally implemented endpoints
# below, it checks PROTECTED_ENDPOINTS and raises an exception if
# the user tries to use one of those. Must be updated if a new endpoint
# is added in this module
#
#
_PROTECTED_ENDPOINTS = ['mon', 'comms', 'passes']

#
# The timestamp label is special in the way it is handled in the database. It can be remapped
# to other names using the below constant.
#
_RETURNED_TSTAMP_LBL = 'tstamp'

#
# Default table styles applied to pd.style
# 
_TABLE_STYLES = [
    dict(selector="tr:nth-child(even)", props=[("background-color", "whitesmoke")]),
    dict(selector="tr:hover", props=[("background-color", "lightyellow")]),
    dict(selector="th", props=[("text-align", "left")]),
    dict(selector="td", props=[("padding", "5px"),
           ('overflow','hidden'),
           ('text-overflow','ellipsis'),
           ('white-space', 'nowrap'),
#           ('white-space','normal'),
#           ('overflow-wrap', 'break-word'),
           ('max-width', '800px')
           ])
]




class RESTAPI(object):
    """
    THE REST API class
    ------------------

    Will create a RESTFUL API interface to the Commslog database and start
    it on a specified port. The api will be started in a separate thread.

    The URI endpoints are:

    /api/comms
      Download the entire communications log

    /api/comms/<sat_id>
      Download the entire communications log for satellite with norad id specified

    /api/comms/<sat_id>/<pass_id>
      Download a specific pass

    Valid parameters are:

    ======== =============================================
    format   output format: json / csv / html
    N        max number of entries to return. Omit for all
    ======== =============================================

    Usage:
      >>> api = RESTAPI()
      >>> api.start()



    """

    def __init__(self,
                 commslog = None,
                 monlog = None,
                 passdb = None,
                 host=Defaults.API_ADDR,
                 port=Defaults.API_PORT,
                 default_format='json',
                 rpcapi = None,
                 allowed=None,
                 retry_rpc_conn = True,
                 debug=True):
        """
        Args:
          commslog (CommsLog)     : Database end-point for comms log
          host     (str)          : Ip address to bind to
          port     (int)          : Port to bind to
          default_format (str)    : Format to provide if no argument given (default = json)
          allowed  (list(str))    : LIst of allowed URI patterns. Default is None, which actually means all
          debug    (bool)         : Set flask in Debug mode for extra verbosity


        """
        self.commslog = commslog #<--- comms db
        self.monlog   = monlog   #<--- monitoring db
        self.passdb   = passdb   #<--- pass db
        self.rpcapi = {}
        self._debug = debug
        self._host = host
        self._port = port
        self._default_format = default_format
        self._abort_event = Event()

        if allowed is not None and not isinstance(allowed, list):
            raise Exception("Invalid type for allowed, expected list, got %s"%(type(allowed)))

        self._allowed = allowed
        _rpcapi = {} if rpcapi is None else rpcapi
        self._rpc_unavailable = {}

        for uri,rpcaddr in _rpcapi.items():
            if uri.split('/')[0] in _PROTECTED_ENDPOINTS:
                raise Exception("{} is a protected endpoint and cannot be used as an rpcapi endpoint".format(uri))
            if uri[-1] == '/':
                uri = uri[:-1]

            try:
                self._try_rpc_connection(uri, rpcaddr)
            except Exception as e:
                self._rpc_unavailable[uri] = rpcaddr
                ags_log.error(
                    "Could not bind to RPC API {}. API not started: ({}: {})".format(uri, e.__class__.__name__, e))

        if retry_rpc_conn:
            self._pthr_connpoll = Thread(target=self._poll_for_rpcconnection)
            self._pthr_connpoll.daemon = True
            self._pthr_connpoll.start()



    def _try_rpc_connection(self, uri, rpcaddr):
        a = dict(addr=uri, server=XMLRPCTimeoutServerProxy(rpcaddr, allow_none=True))

        try:
            # get method from xmlrpc introspection but exclude anything with a . (system methods)
            a['methods'] = [m for m in a['server'].system.listMethods() if m.find('.') < 0]
            ags_log.debug("Bound to RPC API {}. Available methods: {}".format(a['addr'], a['methods']))
            self.rpcapi[uri] = a
        except Exception as e:
            raise



    def _poll_for_rpcconnection(self):

        # try to connect to api every minute
        while len(self._rpc_unavailable) > 0:
            _unavailable = {}
            sys.stdout.flush()
            for uri, rpcaddr in self._rpc_unavailable.items():
                try:
                    self._try_rpc_connection(uri, rpcaddr)
                except Exception as e:
                    _unavailable[uri] = rpcaddr

            self._rpc_unavailable= _unavailable
            if wait_loop(self._abort_event, timeout=60) is not None:
                break


    def _run_api(self):
        with app.app_context():
            current_app.config['API'] = self

        app.run(host=self._host, port=self._port, debug=self._debug, use_reloader=False)

    def start(self):
        self._pthr = Thread(target=self._run_api)
        self._pthr.daemon = True
        self._pthr.start()

        ags_log.info("Started REST API on %s:%d in thread %s"%(self._host, self._port, self._pthr))


    def stop(self):
        pass
        #self._abort_event.set()
        # self._pthr.join(timeout=5)
        # if self._pthr_conpoll.is_alive():
        #     ags_log.error("There was a problem stopping REST API thread")
        # else:
        #     ags_log.info("REST API successfully stopped")


#TODO: Remove from here and move the functionality into the Database class
def tfilterstr2query(filterstr):
    """
    Convert a timestamp filter string into a well formated
    where query
    """

    # mulitiple comma separated filters supported
    filters = filterstr.split(',')

    query = []
    for f in filters:
        if f[0] in ['>', '<']:
            if f[1] == '=':
                op = f[:2]
                f1 = f[2:]
            else:
                op = f[0]
                f1 = f[1:]
        else:
            op = '='
            f1 = f

        try:
            tstamp = to_datetime(f1, yearfirst=True)
        except:
            return None

        query += [op+str(tstamp.to_julian_date())]

    return TSTAMP_LBL + (' AND {}'.format(TSTAMP_LBL)).join(query) + ' '



def handle_bytes(d, format):
    if not isinstance(d, bytearray):
        return d
        
    if format == 'hex':
        return bytes2hex(d)
    elif format == 'b64':
        return b64encode(d)
    elif format == 'b64string':
        return encodestring(d)
    else:
        raise Exception("Invalid format")

def is_allowed(fn):
    """
    This decorator checks if a resource is allowed
    """
    def wrapped(*args, **argv):
        api = current_app.config['API']
        #
        # Check if resource is allowed
        #
        allowed = False
        if api._allowed is not None:
            for c in api._allowed:
                if c == request.path[:len(c)]:
                    allowed = True
                    break

            if not allowed:
                return "Restricted resource", 403

        return fn(*args, **argv)

    wrapped.__name__ = fn.__name__
    return wrapped




@app.route("/api/comms")
@app.route("/api/comms/<sat_id>")
@app.route("/api/comms/<sat_id>/<pass_id>")
@is_allowed
def get_comms(sat_id=None, pass_id=None):

    api = current_app.config['API']
    log = api.commslog

    if log is None:
        return "Resource not available", 403


    form = request.args.get('format')
    if form is None:
        form =api._default_format


    #
    # is the result list going to be limited (N)
    #
    N = request.args.get('N', type=int)

    if N is None:
        ags_log.debug("No N specified, limiting to %d entries"%(DEFAULT_TABLE_LIMIT))
        N = DEFAULT_TABLE_LIMIT

    #
    # allof timestamp filtering
    #
    tfilterstr = request.args.get('tstamp', type=str)

    if tfilterstr is None:
        tfilterquery = None
    else:
        tfilterquery = tfilterstr2query(unquote(tfilterstr))

        if tfilterquery is None:
            msg = 'Invalid timestamp filter string "{}"'.format(tfilterstr)
            return msg, 440

    if sat_id is None:

        if tfilterquery is not None:
            ret = log.get(where=tfilterquery, limit=N)
        else:
            ret = log.get(limit=N)
        ags_log.debug("Actioned api request for full database in format %s"%(form))

    else:
        if tfilterquery is not None:
            tfilterquery += ' AND '
        else:
            tfilterquery = ''
        try:
            sat_id = int(sat_id)
        except:
            msg = "Invalid Norad id"
            ags_log.debug("Invalid API request: %s"%(msg))
            return msg, 440

        if pass_id is None:
            ret = log.get(where=tfilterquery+'NID="{}"'.format(sat_id), limit=N)
            ags_log.debug("Actioned api request for all communications with satellite %s in format %s"%(sat_id, form))
        else:

            try:
                pass_id = int(pass_id)
            except:
                msg = "Invalid pass id"
                ags_log.debug("Invalid API request: %s"%(msg))
                return msg, 440

            ret = log.get(where=tfilterquery+'NID="{}" and PASS_ID="{}"'.format(sat_id, pass_id), limit=N)
            ags_log.debug("Actioned api request for pass %s with satellite %s in format %s"%(pass_id, sat_id, form))


    # ensure table has columns in the right order
    ret = ret[[TSTAMP_LBL, 'nid', 'pass_id', 'orig', 'dest', 'msg']]

    retc = ret.columns.tolist()
    retc[retc.index(TSTAMP_LBL)] = _RETURNED_TSTAMP_LBL
    ret.columns = retc

    #ret = ret.applymap(lambda x: "bytes" if isinstance(x, bytearray) else x)

    if form == 'html':
        ret  = ret.applymap(lambda x: handle_bytes(x, 'hex'))
        ret.pass_id = ['<a href="/api/comms/{}/{}?format=html">{}</a>'.format(r['nid'],r['pass_id'],r['pass_id']) for k,r in ret.iterrows()]
        #return ret.set_index('tstamp').to_html()#escape=False)
        html = html = "<!DOCTYPE html><html><body>" + ret.style.set_table_styles(_TABLE_STYLES).render()
        html += "</body></html>"
        return(html) 

    elif form == 'json':
        ret  = ret.applymap(lambda x: handle_bytes(x, 'b64'))

        rv = app.response_class(
            response=ret.to_json(),
            status=200,
            mimetype='application/json')

        rv.add_etag()
        return(rv)

    elif form == 'csv':
        ret  = ret.applymap(lambda x: handle_bytes(x, 'hex'))
        rv = app.response_class(
            response=ret.set_index(_RETURNED_TSTAMP_LBL).to_csv(),
            status=200,
            mimetype='text/csv')

        rv.add_etag()
        return(rv)


    else:
        return "Invalid format", 440




@app.route("/api/mon")
@app.route("/api/mon/<pass_id>")
@is_allowed
def get_mon(pass_id = None):
    api = current_app.config['API']
    monlog = api.monlog

    if monlog is None:
        return "Resource not available", 403


    # Output format
    form = request.args.get('format')
    if form is None:
        form =api._default_format


    # Keys
    keys = request.args.get('keys')
    if keys is not None:
        keys = keys.split(',')

    # timestamp filtering
    tstamps = request.args.get('tstamps')
    if tstamps is not None:
        tstamps = tstamps.split(',')

    #
    # is the result list going to be limited (N)
    #
    N = request.args.get('N', type=int)
        
    if N is None:
        ags_log.debug("No N specified, limiting to %d entries"%(DEFAULT_TABLE_LIMIT))
        N = DEFAULT_TABLE_LIMIT        

        
    if pass_id is not None:
        ret = monlog.get(pass_id = pass_id, keys=keys, tstamps=tstamps, limit=N)
    else:
        ret = monlog.get(keys=keys, tstamps=tstamps, limit=N)

    retc = ret.columns.tolist()
    retc[retc.index(TSTAMP_LBL)] = _RETURNED_TSTAMP_LBL
    ret.columns = retc

    if form == 'html':
        def highlight_red(data):
            if data['alert'] == 'RED' or data['alert'] == 'CRITICAL':
                ret = ['color: {}'.format('red') for d in data]
            else:
                ret = ['' for d in data]

            return ret

        ret.key = ret.key.apply(lambda v: '<a href="/api/mon?keys={}&format=html">{}</a>'.format(v,v))
        html = "<!DOCTYPE html><html><body>" + ret.style.set_table_styles(_TABLE_STYLES).apply(highlight_red, axis=1).render()
        html += "</body></html>"
        return html
    elif form == 'json':
        rv = app.response_class(
            response=ret.to_json(),
            status=200,
            mimetype='application/json')

        rv.add_etag()
        return(rv)

    elif form == 'csv':
        rv = app.response_class(
            response=ret.set_index(_RETURNED_TSTAMP_LBL).to_csv(),
            status=200,
            mimetype='text/csv')

        rv.add_etag()
        return(rv)


    else:
        return "Invalid format", 440



@app.route("/api/passes")
@app.route("/api/passes/<pass_id>")
@is_allowed
def get_passes(pass_id = None):
    api = current_app.config['API']
    passlog = api.passdb
    commslog = api.commslog

    if passlog is None:
        return "Resource not available", 403


    # Output format
    form = request.args.get('format')
    if form is None:
        form =api._default_format


    # Keys
    keys = request.args.get('keys')
    if keys is not None:
        keys = keys.split(',')

    # timestamp filtering
    tstamps = request.args.get('tstamps')
    if tstamps is not None:
        tstamps = tstamps.split(',')

    #
    # is the result list going to be limited (N)
    #
    N = request.args.get('N', type=int)
        
    if N is None:
        ags_log.debug("No N specified, limiting to %d entries"%(DEFAULT_TABLE_LIMIT))
        N = DEFAULT_TABLE_LIMIT        

        
    if pass_id is not None:
        ret = passlog.get(pass_id = pass_id, keys=keys, tstamps=tstamps, limit=N)
    else:
        ret = passlog.get(keys=keys, tstamps=tstamps, limit=N)

    retc = ret.columns.tolist()
    retc[retc.index(TSTAMP_LBL)] = _RETURNED_TSTAMP_LBL
    ret.columns = retc
        
    if form == 'htmlraw':
        ret = ret.applymap(lambda x: handle_bytes(x, format='b64'))
        ret.pass_id = ret.pass_id.apply(lambda x: '<a href="/api/passes/{}?format=html">{}</a>'.format(x,x))
        html = "<!DOCTYPE html><html><body>" + ret.style.set_table_styles(_TABLE_STYLES).render()
        html += "</body></html>"
        return html
    elif form == 'html':

        # pivot the table
        ret = ret.pivot(index='pass_id', columns='key', values='value')
        ret = ret.applymap(lambda x: handle_bytes(x, format='b64'))
        ret = ret.sort_index(ascending=False)
        cols = ['norad_id', 'start_t', 'start_track_t', 'end_track_t', 'stowed_t', 'max_el']
        cols = cols + [c for c in ret.columns if c not in cols]
        for c in cols:
            if c not in ret.columns:
                ret[c] = None
                
        ret = ret[cols]

        if 'waterfall_jpeg' in cols:
            def add_link(s):
                if not isinstance(s, basestring):
                    return s

                if s[:7] == 'file://':
                    return ("<a href='/api/file/passes/{}?format=jpeg'>download</a>".format(s[7:]))
                else:
                    return ("<a href='data:image/jpeg;base64,{}'>download</a>".format(s))

            ret.waterfall_jpeg = ret.waterfall_jpeg.apply(add_link)
            
        if 'schedule' in cols:
            def add_link(s):
                if not isinstance(s, basestring):
                    return s

                if s[:7] == 'file://':
                    return ("<a href='/api/file/passes/{}'>download</a>".format(s[7:]))
                else:
                    return ("<a href='data:application/json,{}'>download</a>".format(s))
                
            ret.schedule = ret.schedule.apply(add_link)

        def nid_to_int_if_possible(nid):
            try:
                return int(nid)
            except:
                return nid

        if 'signoffs' in cols:
            ret.signoffs = [', '.join(s) if isinstance(s, list) else s for s in ret.signoffs]

        ret['norad_id'] = [nid_to_int_if_possible(nid) for nid in ret['norad_id']]

        #
        # add some meta columns
        #

        # this adds the number of comms...
        #    ret['comms'] = [len(commslog.get(where='PASS_ID="{}"'.format(p))) for p in ret.index]

        ret['comms'] = ["<a href='/api/comms/{}/{}?format=html'>go</a>".format(nid_to_int_if_possible(ret.norad_id[pid]), pid) for pid in ret.index]
        ret['monitoring'] = ["<a href='/api/mon/{}?format=html'>go</a>".format(pid) for pid in ret.index]
        
        
        def format_time(t):
            try:
                return conv_time(t, to='datetime').strftime('%Y-%m-%d %H:%M:%S')
            except:
                return None

        ret[['start_t', 'start_track_t', 'end_track_t', 'stowed_t']] = ret[['start_t', 'start_track_t', 'end_track_t', 'stowed_t']].applymap(format_time)


        html = "<!DOCTYPE html><html><body>" + ret.style.set_table_styles(_TABLE_STYLES).render()
        html += "</body></html>"
        return html
        
    elif form == 'json':
        ret = ret.applymap(lambda x: handle_bytes(x, format='b64'))
        rv = app.response_class(
            response=ret.to_json(),
            status=200,
            mimetype='application/json')

        rv.add_etag()
        return(rv)

    elif form == 'csv':
        ret = ret.applymap(lambda x: handle_bytes(x, format='b64'))        
        rv = app.response_class(
            response=ret.set_index(_RETURNED_TSTAMP_LBL).to_csv(),
            status=200,
            mimetype='text/csv')

        rv.add_etag()
        return(rv)


    else:
        return "Invalid format", 440


@app.route("/api/file")
@app.route("/api/file/<dbname>")
@app.route("/api/file/<dbname>/<fname>")
@is_allowed
def get_file(dbname=None, fname=None):

    if dbname is None or fname is None:
        return "Invalid DB / FILE" , 403

    api = current_app.config['API']        
    
    if dbname == 'comms':
        db = api.commslog
    elif dbname == 'mon':
        db = api.monlog
    elif dbname == 'passes':
        db = api.passdb
    else:
        return "Invalid database", 403
        
        
    try:
        data = db.get_file(fname)
    except:
        return "Invalid file", 403
    

    form = request.args.get('format')
    
    if isinstance(data, basestring):

        # TODO: FIX THIS !!!
        # What's going on here is that the json is doubly encoded. In the past there wasnt much of a way around that
        # but lately we are prefixing json stuff with json:// so we should be able to get away from this.
        # Anyway, for now just hack it to remove the type indicator.
        #
        if data[:7] == 'json://':
            data = data[7:]

        rv = app.response_class(
            response=json.loads(data),
            status=200,
            mimetype='application/json')

        return rv

        
    if form == "jpg" or form == "jpeg":
        rv = app.response_class(
            response=data,
            status=200,
            mimetype='image/jpeg')

        return rv

    else:
        ret = handle_bytes(data, 'b64string')
        rv = app.response_class(
            response=json.dumps(ret),
            status=200,
            mimetype='application/json')

        return rv
        


@app.route("/api/<path:path>")
@is_allowed
def get_rpcapi(path):
    """
    Invoke a (user-defined) RPC API. 
    
    Usage:
       /api/<name>[/method]
      
    Args:
       name             : can have several levels; eg. "test/subtest/etc" or not "test"
       method (optional): The RPC method to call (if not supplied return available methods)
    
    """
    try:
        api = current_app.config['API']
        rpcapi = api.rpcapi


        def guess_arg_type(inp):
            try:
                out = float(inp)
            except:
                out = str(inp)

            return out

        name = None
        for apiname in rpcapi.keys():
            if path.find(apiname.strip()) == 0:
                name = apiname.strip()
                args = path[len(apiname)+1:].strip().split('/')
                method = args[0].strip()
                args = [guess_arg_type(a) for a in args[1:]]
                break

        status = 200

        if name is None:
            status = 403
            ret =  "Invalid resource {}"
        elif name not in rpcapi.keys():
            status = 403
            ret = "Invalid RPC API endpoint '{}'. Available are {}".format(name, rpcapi.keys())
        elif method == '':
            ret = rpcapi.keys()
        else:

            r = rpcapi[name]

            if method is None or method == '':
                ret = r['methods']

            elif method not in r['methods']:
                status = 403
                ret = "Method '{}' not available. Available: {} ".format(method, r['methods'])
            else:
                kwargs = {k:guess_arg_type(v) for k,v in request.args.items()}

                try:
                    ret = getattr(rpcapi[name]['server'], method)(*args, **kwargs)
                except Exception as e:
                    ret = dict(description="Exception while making RPC call. Most likely reason is that the RPC function does not return a marshallable type. (See https://docs.python.org/2/library/xmlrpclib.html), or passed arguments are invalid.",
                               exc_type = e.__class__.__name__,
                               exception = str(e))

                    status = 500

        # if method returned valid json, dont jsonify again, otherwise do so
        try:
            json.loads(ret)
            retj = ret
        except:
            try:
                retj = json.dumps(ret)
            except Exception as e:
                raise

    except Exception as e:
        retj = json.dumps(dict(exc_type=e.__class__.__name__, exception=str(e)))
        status = 500

    rv = app.response_class(
        response=retj,
        status=status,
        mimetype='application/json')
    
    return rv
    
    
    
        

@app.route("/", strict_slashes=False)
@app.route("/api", strict_slashes=False)
@is_allowed
def get_help():
    api = current_app.config['API']
    rpcapi = api.rpcapi
    
    html = """
 <!DOCTYPE html>
<html>
<body>
<h2> libgs api </h2>
{REPLACE_ME_COMMS}
{REPLACE_ME_MON}
{REPLACE_ME_PASSES}
{REPLACE_ME_RPC}
</body>
</html> 

"""

    # TODO: Get helps from docstrings


    #
    # COMMS DB API
    #
    helptxt =  "<h3> Comms DB API </h3>"
    helptxt += "<p>Syntax: <pre> /api/comms/{norad id}/{pass id}?format={html,json,csv}&N={N}&tstamp={tstamp filter}</pre>"
    helptxt += "<br/> Example: <a href=/api/comms?format=html>/api/comms?format=html</a>: Get all communications (N is limited by default, increase explicitly to get more values)"
    helptxt += "</p>"
    html =  html.replace('{REPLACE_ME_COMMS}', (helptxt))
    
    #
    # Monitor DB API
    #
    helptxt = "<h3> Monitor DB API </h3>"
    helptxt += "<p> Syntax: <pre> /api/mon{/pass id}?format={html,json,csv}&N={N},keys={keypattern,keypatern,...} </pre>"   
    helptxt += r"<br/> keypattern supports % as a wildchar"
    helptxt += r"<br/> Example: <a href=/api/mon?format=html> /api/mon?format=html </a>: Get all monitoring data (N limited by default, set N=explicitly to increase)" 
    helptxt += r"<br/> Example: <a href=/api/mon?keys=%RACK%,%5V%&format=html>/api/mon?keys=%RACK%,%5V%&format=html </a>: Get all RACK and 5V telemetry points"
    helptxt += r"</p>"
    html =  html.replace('{REPLACE_ME_MON}', (helptxt))
    
    #
    # Pass DB API
    #
    helptxt = "<h3> Passes DB API </h3>"
    helptxt += "<p> Syntax: <pre> /api/passes{/pass_id}?format={htmlraw, html, json, csv}{&N=N}{&keys=keypattern,...}</pre>"
    helptxt += r"<br/> keypattern supports % as a wildchar"
    helptxt += r"<br/> Example: <a href=/api/passes?format=html> /api/passes?format=html </a>: Get all pass data (N limited by default, set N=explicitly to increase)" 
    html = html.replace("{REPLACE_ME_PASSES}", (helptxt))
    
    #
    # RPC help
    #
    helptxt =  "<h3> Other APIs </h3>\n"
    helptxt += "<p>Syntax: <pre>/api/{endpoint}/{method}[?{arg1}&{arg2}&{arg3} ...]</pre></p>"
    helptxt += "<ul>"
    
    for k,v in rpcapi.items():
        helptxt +=  "<li><pre> endpoint = {}, avail methods = {} </pre></li>".format(k, v['methods'])
    helptxt += "</ul>"
    html =  html.replace('{REPLACE_ME_RPC}', (helptxt))
    
    return html, 200



if __name__=='__main__':
    pass