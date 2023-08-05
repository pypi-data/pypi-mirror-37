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



ADFA-GS Visualisation module
============================

:date: Mon Jul 17 16:38:56 2017
:author: kjetil

Overview
-----------

This module contains wraps a bunch of Bokeh code focused at  craeting
the different plots and web-apps useful for ADFAGS. In particular
* Spectrum
* Waterfall
* Tracking status
* Dashboard

However it is written in a generic way as a standalone API
that could be useful for other applications.

While based on Bokeh, it does not require the Bokeh server to run. Rather the
Bokeh server is initiated from within this module. For that reason the syntax
for "live" elements (Plots and Widgets) is slightly different to the most common
examples in the Bokeh documentation.


The plots and elements in this module can be updated dynamically.

Implementation
----------------

All plots are derived from LivePlot and shall implement the following method
* create_fig(self, sources): Shall return a Bokeh figure.

And may implement the following attributes if required. Data
registered in live_data will be passed onto the figure ColumnDataSource
using the same mapping. And properites in live_props will be updated
on the figures as well.

* live_data (type: dict)
* live_props (type: dict)


BokehDash and its derived class(es) implment the Bokeh Server and keeps
track of the different plots that are added to it. When the web-page is
requested by a client, it will construct a document for each client using the
individual plots'get_fig function.

It will also create ColumnDataSources for those figures, and in a regular
callback loop, keep everything up to date with the live_data and live_props
dictionaries in the different plots.

With this implementation, it is possible to have multiple clients connect at
the same time and see the same data while not having to run bokeh as a separate
application.


"""

# Create Tornado IOLoop
from tornado.ioloop import IOLoop
import threading

#import time
import random
import bokeh
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import Figure, ColumnDataSource
import bokeh.layouts as bl
import string
import zmq
import requests
from bokeh.models.widgets import PreText, Div, Paragraph
from numpy import sin, cos, pi
import numpy as np
from bokeh.models import LabelSet, Label#, HoverTool
import colorsys
import time, datetime
from utils import Defaults, RegularCallback

import logging
log = logging.getLogger('adfags-log')
log.addHandler(logging.NullHandler())
"""
 Configure logging with the name adfags-log, and add the NullHandler. That
 means that log messages will be dropped unless the application using this
 library configures logging.
"""


#
# Prevent tornado for polluting the root handler.
# TODO: Configure tornados own logger (tornado.access) to ge the log messages
#
logging.getLogger().addHandler(logging.NullHandler())

class Error(Exception):
    """Generic Error for this module"""

    def __init__(self, msg, original_Error=None):
        if original_Error is not None:
            super(Error, self).__init__(msg + (": %s" % original_Error))
            self.original_Error = original_Error
        else:
            super(Error, self).__init__(msg)


def linktext(links):
    """
    Convenience function to create a series of navigation links to use on the top
    of the different apps
    """

    if 1:
        linktxt = ''
        for link in links:
            if len(link) == 2:
                link = (link[0], link[1], None)

            if len(link) != 3:
                raise Error("Invalid link argument")

            if linktxt != '':
                linktxt += ' | '

            if link[2] is not None:
                linktxt += '<a href="%s" onclick="javascript:event.target.port=%d">%s</a>'%(link[1], link[2], link[0])
            else:
                linktxt += '<a href="%s">%s</a>'%(link[1], link[0])


    return linktxt

def azel2rect(az, el):
    """
    Helper-function to conver az,el (polar coordinates) to x,y
    for display on rectangular axes

    """
    if az is None or el is None:
        return None, None

    # Check if az and el are arrays or scalars
    # convert to arrays if scalar
    try:
        len(az)
    except TypeError:
        az = [az]

    try:
        len(el)
    except TypeError:
        el = [el]

    if len(az) != len(el):
        raise Error('az and el must be of same lenght')

    az = 360.0 - np.array(az)
    el = np.array(el)
    x = (90-el)*cos((az+90)/180.0*pi)
    y = (90-el)*sin((az+90)/180.0*pi)
    return x,y

class LivePlot(object):
    """
    Base class for all the plots.

    All derived classes shall implent the following method
    * create_fig(self, sources): Shall return a Bokeh figure.

    And may implement the following attributes if required. Data
    registered in live_data will be passed onto the figure ColumnDataSource
    using the same mapping. And properites in live_props will be updated
    on the figures as well.

    * live_data (type: dict)
    * live_props (type: dict)


    """

    live_data = dict()
    live_props = dict()

    def __init__(self):
        pass

    def __get_name__(self):
        # TODO: This doesnt actually work. Fix
        if not hasattr(self, 'name'):
            self.name="liveplot-"+ ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        else:
            return self.name

    def create_fig(self, sources):
        raise Error('create_fig(self,sources) must be overloaded')
        # live plots


class SatellitePass(LivePlot):
    """
    Visualisation of the sky.

    Can show, in real-time, the current and demanded pointing of the
    antennas, the satellite track, and the position of the tracked satellite

    Attr:
        name: A descriptive (and unique) name. Required for the Bokeh server
        live_data: The datapoints that can be updated in real-time
        live_props: The properties that can be updated in real-time

    The following live_data is used:

    """


    def __init__(self, name, **fig_args):
        self.name=name
        self.live_data = dict(
            ant_cur = {
                'x': [10],
                'y': [0]},

            ant_cmd = {
                'x': [10],
                'y': [10]},

            sat = {
                'x': [0],
                'y': [0]},

            dpass = {
                'x': [0,90,0,0],
                'y': [0,0,90,0]}
                )

        # Figure arguments
        self._fig_args = fig_args


    def create_fig(self, sources):
        fig = Figure(background_fill_color= None,
                     toolbar_location = None,
                     x_range=[-100, 100], y_range=[-100, 100], tools="", **self._fig_args)



        # Remove existing axes and grid
        fig.xgrid.grid_line_color = None
        fig.ygrid.grid_line_color = None
        fig.axis.visible = False


        # Draw circular grid
        th = np.linspace(0, 360, 100)

        # Draw visibility field
        self.vis_horizon = 10
        #fig.patch(*pol2rect([90 - self.vis_horizon]*len(th), th), color='lightgray')
        fig.patch(*azel2rect(th, [self.vis_horizon]*len(th)), color='lightgray')


        for r in [0, 20, 40, 60, 80]:
            fig.line(*azel2rect(th, [r]*len(th)), line_dash='dashed')

        for th in np.arange(0,360,45):
            fig.line(*azel2rect([th,th], [0,90]), line_dash='dashed')

        # Add grid labels
        lx,ly = azel2rect([0, 90, 180, 270], [0]*4)
        lx[1] -= 30
        lx[2] -= 20
        ly[0] -= 10
        lx[0] -= 10
        src_labels = ColumnDataSource(dict(
            labels= ['N (0)', 'E (90)', 'S (180)', 'W (270)'],
            label_x= lx,
            label_y =ly))

        fig.add_layout(LabelSet(x='label_x', y='label_y', text='labels', source=src_labels))



        fig.line(source=sources['dpass'], x='x', y = 'y', line_width=2)
        fig.circle(source=sources['ant_cmd'], x='x', y='y', size=20, fill_color=None)
        fig.circle(source=sources['ant_cur'], x='x', y='y', size=10, color='green')
        fig.circle(source=sources['sat'], x= 'x', y ='y', size=10, color= 'yellow')

        return fig




    def plot_pass(self,az, el):
        """
        Convenience function for plotting a pass
        """
        x, y = azel2rect(az, el)
        self.live_data['dpass'] = dict(x=x,y=y)

    def update_data(self, dataset, az, el):
        """
        Convenience function for updating any live_data element

        Args:
            dataset (string): The live_data to update. dataset='dpass' is equivalent
                              to calling plot_pass
        """
        # Todo: programmatic for any dataset
        if dataset not in self.live_data.keys():
            raise Error("Invalid dataset")

        x, y = azel2rect(az, el)

        self.live_data[dataset] = dict(x=x, y=y)

class BokehServer(object):
    """
        A class to set up and run the bokeh server to serve the dashboard apps.

        Apps need to be added to the server using the add_app method

        Args:
            port (int, optional): The port to run the webserver on


    """

    def __init__(self, port=5001, host='127.0.0.1'):
        self._loop= IOLoop()
        self._apps = {}
        self._bokeh_port = port
        self._bokeh_host = host


    def add_app(self, uri, makefn):
        if isinstance(makefn, BokehApp):
            makefn = makefn._make_doc
        elif not callable(makefn):
            raise Error("App must either be of type BokehApp (i.e. with a _make_doc method), or a callable")

        self._apps[uri] = Application(FunctionHandler(makefn))


    def start(self):
        """
            Starts the server and tornado IOloop. This is required for the plots
            to become live.
        """
        
        self._server = Server(self._apps, address=self._bokeh_host, port=self._bokeh_port, loop=self._loop, allow_websocket_origin=["*"])

        self._server.start()

        self._ploop = threading.Thread(target=self._loop.start)
        self._ploop.daemon = True
        self._ploop.start()

        # Now request the page so that all the figures get initialised

        for uri in self._apps.keys():
            url = "http://%s:%d%s"%(self._bokeh_host, self._bokeh_port, uri)
            log.debug("Initialising app on %s"%(url))
            requests.get(url)


    def stop(self):
        """
            Stops the tornado IOloop (does not do anything with the server)

            ..todo::
              Properly stop server too
        """


        self._loop.stop()
        self._ploop.join()

        for plot in self._plots:
            if hasattr(plot, 'disconnect'):
                plot.disconnect()



class BokehApp(object):
    """
    Base class for any bokeh application
    """

    def _make_doc(self, doc):
        raise Error("_make_doc has not been implemented")

class BokehDash(BokehApp):
    """
        A bare-bone Bokeh dashboard app aimed at ADFA GS.

        Plots and Visualisations can be added to the Dashboard using the add_plot
        method.

        The app sets up its own Bokeh server and Tornado IOloop and is therefore
        able to run completely independently.

        Args:
            port (int, optional): The port to run the webserver on
            update_rate (float, optional): The delay (in seconds) between each update of
                        the dashboard (on the client-side)
            title (string, optional): The dashboard title
            layout_callback (function, optional): An optional function that defines
                        the layout using bokeh.layout elements. The layout_callback function
                        shall accept a single argument being a list of figures.
                        It shall return a layout comprising those figures.


    """

    def __init__(self,  update_rate=0.1, title="Bokeh-based dashboard", layout_callback=None):
        self._title_text = title

        # set update rate (in ms)
        self._update_rate = int(update_rate * 1000)

        # plots
        self._plots = []

        # Layout function
        self._layout_callback = layout_callback



    def add_plot(self, plot):
        """
            Add a live plot to the document
        """

        self._plots.append(plot)


    def get_plot(self, name):
        """
        Return a plot by name
        """

        for p in self._plots:
            if p.name == name:
                return p

        raise Error('Plot does not exist')

    def _create_title_fig(self):
        fig = Figure(sizing_mode='scale_width',
             x_range=[0, 1], y_range=[0,1], plot_height=50, tools="")

        # Remove existing axes and grid
        fig.xgrid.grid_line_color = None
        fig.ygrid.grid_line_color = None
        fig.axis.visible = False
        fig.background_fill_color= None
        fig.toolbar_location = None

        text = Label(x=0.5, y=0.5,
            text=self._title_text, render_mode='css',
            background_fill_color='white', background_fill_alpha=1.0,
            text_font_size='28pt', text_align='center', text_baseline= 'middle'
            )

        fig.add_layout(text)


        return(fig)


    def _make_doc(self, doc):
        """
            Set up the document. This function is called once for each
            client connection.

            Variables are therefore kept local in this scope rather than
            added to the class as method which would have meant that multiple
            users were served the same variable (ColumnDataSource or Figure)
            something that is not permitted by Bokeh.

        """
        titlefig = self._create_title_fig()

        clock = Paragraph(text="A clock")


        datasrc = {}

        for plot in self._plots:
            datasrc[plot.__get_name__()] = dict()
            for data_key, data in plot.live_data.items():
                datasrc[plot.__get_name__()][data_key] = ColumnDataSource(data)

        # Create a dot that continually changes colour to show that app is live
        src_heartbeat = ColumnDataSource(dict(x=[0.01],y=[0.9],color=['red']))
        hb_cols = [bokeh.colors.RGB(*np.array(colorsys.hsv_to_rgb(a,1,1))*255) for a in np.linspace(0,1,40)]

        def update():

            # Update heartbeat
            update.counter = (update.counter + 1)%len(hb_cols)
            src_heartbeat.data['color'] = [hb_cols[update.counter]]

            # Update clock
            clock.text = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            # Update everything else
            for plot in self._plots:
                for data_key, data in plot.live_data.items():
                    datasrc[plot.__get_name__()][data_key].data = data

                for prop, data in plot.live_props.items():
                    setattr(figs[plot.__get_name__()], prop, data)

        update.counter = 0

        # Set update frequency
        doc.add_periodic_callback(update, self._update_rate)

        # Set up the figures, and plot anything that is static
        #
        # WARNING: Using self.figs here is probably dangerous
        #  Since I believe a new figs object needs to be created
        #  at every reload.
        figs = dict()
        for plot in self._plots:
            figs[plot.__get_name__()] = plot.create_fig(datasrc[plot.__get_name__()])

        # Draw heartbeat
        titlefig.circle(source=src_heartbeat, x='x', y='y',  color='color', size=10)

         # Lay everything out
        if self._layout_callback is None:
            layout = bl.layout([[titlefig,clock], figs.values()], sizing_mode='scale_width')
        else:
            layout = bl.column([titlefig,clock, self._layout_callback(figs)], sizing_mode='scale_width')

        doc.add_root(layout)

        doc.title = self._title_text




class FrequencyPlot(LivePlot):

    def __init__(self, name, get_spectrum, wfall=None,  title=None, **fig_args):
        self.live_data = {'freq': {'x': [], 'y':[]}}
        self.name = name
        self._get_spectrum = get_spectrum

        #Figure title
        self._fig_title = title if title is not None else name

        # Figure arguments
        self._fig_args = fig_args

        # The waterfall to connect spectrum to
        self._wfall_plot = wfall
        
        # Rate at which to update spectrum
        self._update_delay = Defaults.VIS_FREQUENCY_PLOT_UPDATE_DELAY



    def _update_plots(self):
        try:
            x, y = self._get_spectrum(old=False)
        except:
            return
    
        self.live_data['freq'] = {'x':x, 'y':y}
   
        if self._wfall_plot is not None:
            self._wfall_plot.add_freq_plot(y)
            

    def create_fig(self, sources):

        self._sample_rate = 32000
        self._freq=0
        fig = Figure(logo=None, **self._fig_args)

        fig.line(source=sources['freq'], x='x', y = 'y')
        fig.xaxis.axis_label = "Frequency (MHz)"
        if self._fig_title is not None:
            fig.title.text = self._fig_title

        fig.x_range.range_padding = 0

        return(fig)

    def connect(self):
        self._regcb = RegularCallback(self._update_plots, delay=self._update_delay)
        self._regcb.start()

    def disconnect(self):
        if hasattr(self, '_regcb'):
            self._regcb.stop()

class FrequencyPlot_TODELETE(LivePlot):

    def __init__(self, name, sample_rate = 8*9600, freq=0, gr_addr='127.0.0.1:5551', wfall=None, fftsize=1024,  **fig_args):
        self.live_data = {'freq': {'x': [], 'y':[]}}
        self.name = name
        self._sample_rate = sample_rate#8*9600#float(sample_rate)
        self._freq = freq
        self._gr_addr = "tcp://%s"%(gr_addr)

        self._stop_recv = False

        # Timeout while waiting for a receive
        self._poll_timeout = 1000

        # Figure arguments
        self._fig_args = fig_args

        #
        self._wfall_plot = wfall


        self._fftsize = fftsize

        #print (name, self._sample_rate, self._freq)

	self.min_update_delay=0.25
	self.t0 = time.time()

    def _recv_thread(self):

        poller = zmq.Poller()
        poller.register(self._sock, zmq.POLLIN)

        # Stay in thread until stop_recv is set to true
        while (self._stop_recv == False):
            sock = poller.poll(self._poll_timeout)
            for s, event in sock:
                data = s.recv()
                if time.time() - self.t0 < self.min_update_delay:
                    break
                y = np.frombuffer(data, dtype=np.complex64)
                #y = y - y.mean() # remove DC
                y = 20*np.log10(abs(np.fft.fftshift(np.fft.fft(y, n=self._fftsize))))
                x = np.fft.fftfreq(len(y), d = 1.0/self._sample_rate)
                x = (np.fft.fftshift(x) + self._freq)/1e6
                self.live_data['freq'] = {'x':x, 'y':y}
		self.t0 = time.time()


                if self._wfall_plot is not None:
                    self._wfall_plot.add_freq_plot(y)

    def create_fig(self, sources):

        #hover = HoverTool(tooltips=("Pos", "$x, $y"))
        fig = Figure(logo=None, x_range=[(-self._sample_rate/2.0 + self._freq)/1e6, (self._sample_rate/2.0 + self._freq)/1e6],# tools=[hover],
                     **self._fig_args)

        fig.line(source=sources['freq'], x='x', y = 'y')
        fig.xaxis.axis_label = "Frequency (MHz)"
        #fig.yaxis.axis_label = "dB (arbitrary)"

        return(fig)

    def connect(self):
        self._context = zmq.Context()
        self._sock = self._context.socket(zmq.SUB)
        self._sock.connect(self._gr_addr)
        self._sock.setsockopt(zmq.SUBSCRIBE, '')

        self._stop_recv = False
        self._pthr = threading.Thread(target = self._recv_thread)
        self._pthr.daemon = True
        self._pthr.start()

    def disconnect(self) :
        if hasattr(self, '_pthr'):
            self._stop_recv = True
            self._pthr.join()




class Waterfall(LivePlot):

    def __init__(self, name, sample_rate, freq=0,  wfallwidth=128, wfallheight=100, **fig_args):
        self.live_data = {'wfall': { 'image':[np.random.random((wfallheight,wfallwidth))]}}
        self.name = name
        self._sample_rate = sample_rate
        self._freq = freq
        self._height = wfallheight
        self._width = wfallwidth
        self._fig_args = fig_args

    def create_fig(self, sources):
        fig = Figure(logo=None,
                     x_range=[-self._sample_rate/2.0, self._sample_rate/2.0],
                    y_range=[0,self._height], **self._fig_args)

        fig.image('image', source= sources['wfall'], x=-self._sample_rate/2.0, y = 0, dw=self._sample_rate,dh=self._height,palette=Defaults.WFALL_COLORMAP )

        fig.xgrid.grid_line_color = None
        fig.ygrid.grid_line_color = None
        fig.axis.visible = False


        #fig.xaxis.axis_label = "Frequency"
        #fig.yaxis.axis_label = "dB (arbitrary)"

        return fig

    def add_freq_plot(self, freq):

        if self._width < len(freq):
            if  len(freq) % self._width != 0:
                raise Error('frequency vector must be a multiple of waterfall width')
            else:
                freq = np.array(freq).reshape((-1, len(freq)/self._width))
                freq = freq.max(1)

        if self._width != len(freq):
            raise Error('Dimension mismatch')

        data = self.live_data['wfall']['image'][0]
        if data.shape[0] < self._height:
            self.live_data['wfall']['image'] = [np.concatenate((data, [freq]))]
        else:
            self.live_data['wfall']['image'] = [np.concatenate((data[1:,:], [freq]))]


class Markup(LivePlot):
    """
        An wrapper for the three Bokeh Markup widgets.
    """

    def __init__(self, name, text, mtype='PreText', **args):
        self._text = text
        self.name = name
        self.live_props = {'text': text}
        self.live_data = {}
        self._args = args

        if mtype not in ['PreText', 'Div', 'Paragraph']:
            raise Error('Invalid mtype')

        self._type = mtype

    def create_fig(self, sources):

        if self._type == 'PreText':
            fig = PreText(text=self._text,  **self._args)
        elif self._type == 'Div':
            fig = Div(text=self._text, **self._args)
        elif self._type == 'Paragraph':
            fig = Paragraph(text=self._text, **self._args)

        return fig


class TrackDash(BokehDash):


    UNITS = 50

    def __init__(self,  radios=[], title="Groundstation Dashboard", links=[]):

        UNITS = self.UNITS
        WFALLH = 5*UNITS
        FREQH = 5*UNITS

        # Radio plots - freqency and waterfalls
        wfall = []
        freq = []

        i = 1
        for radio in radios:

            wfall.append(Waterfall('wfall%d'%(i), 32000, 0, plot_height=WFALLH, toolbar_location=None))
            freq.append(FrequencyPlot('freq%d'%(i), radio.get_spectrum, wfall=wfall[-1], title = radio.name, plot_height=FREQH, tools="hover"))
            freq[-1].connect()
            i +=1

        # Satellite pass visualisation
        spass = SatellitePass('spass', plot_height=5*UNITS, plot_width=5*UNITS)

        # Textbox for tracking info
        track_info  = Markup('track_info', mtype='Div', text='', width=500)

        # Tetbox for schedule info
        sch_info = Markup('sch_info', text='')


        # Links along the top to different apps
        linksbox = Markup('links', mtype='Div', text=linktext(links))


        #
        # Create a custom layout to make things look nice
        #
        def layout_figs(figs):

            #row1 = bl.row([figs['title']], sizing_mode='scale_width')
            row2 = bl.row([figs['links']], sizing_mode='scale_width')
            row3 = bl.row([figs['spass'], figs['track_info']], sizing_mode='fixed')

            radios = []

            for i in range(1, len(wfall)+1):
                radios.append(bl.column([figs['freq%d'%(i)],figs['wfall%d'%(i)]], sizing_mode='scale_width'))


            row4 = bl.row(radios, sizing_mode='scale_width')
            row5 = bl.row([figs['sch_info']], sizing_mode='scale_width')

            layout = bl.column([row2,row3,row4, row5], sizing_mode='scale_width')

            return layout

        super(TrackDash, self).__init__(layout_callback=layout_figs, title=title)

        #
        # Now add everything to the dashboard
        #
        for wf in wfall:
            self.add_plot(wf)

        for f in freq:
            self.add_plot(f)

        self.add_plot(spass)
        self.add_plot(track_info)
        self.add_plot(linksbox)
        self.add_plot(sch_info)


class TextDash(BokehDash):
    """
    A simple Dash app that just contains a single text box
    """

    def __init__(self, title, plot_name, mtype='PreText',  links=[]):


        if plot_name == 'links':
            raise Error("Plot name cannot be links")

        linksbox = Markup('links', mtype='Div', text=linktext(links))

        textbox  = Markup(plot_name, mtype=mtype, text='')


        #
        # Create a custom layout to make things look nice
        #
        def layout_figs(figs):

            row1 = bl.row([figs['links']], sizing_mode='scale_width')
            row2 = bl.row([figs[plot_name]], sizing_mode='scale_width')
            layout = bl.column([row1,row2], sizing_mode='scale_width')

            return layout

        super(TextDash, self).__init__(layout_callback=layout_figs, title=title)


        self.add_plot(linksbox)
        self.add_plot(textbox)



if __name__=='__main__':

    if 1:
        from adfags import Radio, Defaults
        server = BokehServer()
        radios = [\
                Radio('UHF TX', Defaults.RADIO_INTS['UHFTX']),
                Radio('UHF RX', Defaults.RADIO_INTS['UHFRX']),
                Radio('SBAND', Defaults.RADIO_INTS['SBAND'])]
        dash = TrackDash(radios=radios)
        statdash = TextDash(plot_name='hwstatus')
        servdash = TextDash(plot_name='servstatus')

        server.add_app('/', dash)
        server.add_app('/status', statdash)
        server.add_app('/services', servdash)
        server.start()
