#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License <https://opensource.org/licenses/MIT>
#
# Copyright (C) 2018 Praveen Kumar.
# Copyright (C) 2017-2018 -- mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


from __future__ import print_function
import argparse
import configparser
import os
import sys

import requests
import urllib3
import vlc

from pycocoa import (
    NSAlternateKeyMask,
    NSApplication,
    NSBackingStoreBuffered,
    NSCommandKeyMask,
    NSControlKeyMask,
    NSMenu,
    NSMenuItem,
    NSRect4_t,
    NSScreen,
    NSShiftKeyMask,
    NSSize_t,
    NSStr,
    NSView,
    NSWindow,
    NSWindowStyleMaskUsual,
    ObjCClass,
    ObjCInstance,
    ObjCSubclass,
    PyObjectEncoding,
    get_selector,
    send_super_init,
)

try:
    from math import gcd  # Python 3+
except ImportError:
    try:
        from fractions import gcd  # Python 2-
    except ImportError:
        def gcd(a, b):
            while b:
                a, b = b, (a % b)
            return a


class VSOMSession(object):
    def __init__(self, url, username, password, verify=True):
        self._base_url = '{}/ismserver/json'.format(url)
        self._session = requests.Session()
        self._session.verify = verify
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._login(username, password)

    def _post(self, url, data):
        response = self._session.post('{}/{}'.format(self._base_url, url),
                                      json=data)
        if not response.ok:
            raise UserWarning('POST failed, code: {}; body: {}'.format(
                response.status_code, response.text
            ))
        parsed = response.json()
        if parsed["status"]["errorType"] != "SUCCESS":
            raise UserWarning('POST failed, response: {}'.format(
                response.text))
        return parsed

    def _login(self, username, password):
        data = {
            "username": username,
            "password": password,
        }
        self._post('authentication/login', data)

    def get_cameras(self):
        data = {
            "filter": {
                "byObjectType": "device_vs_camera",
                "pageInfo": {
                    "start": "0",
                    "limit": "100",
                },
            },
        }
        response = self._post('camera/getCameras', data)
        return dict(map(
            lambda i: (i["videoController"]["deviceRef"]["refName"],
                       i["videoController"]["deviceRef"]["refUid"]),
            response["data"]["items"]
        ))

    def get_stream(self, uid):
        data = {
            "cameraStreamingDetailsRequest": {
                "cameraRefs": [
                    {
                        "refUid": uid,
                        "refObjectType": "device_vs_camera_ip"
                    }
                ],
                "tokenExpiryInSecs": 28800,
                "requestedStreams": "videostream1",
                "recordingStartTimeInSecs": 0,
                "tokenType": "h2",
                "loadStreamProfile": True
            }
        }
        response = self._post('camera/getStreamingDetails', data)
        details = response["data"]["cameraStreamingDetails"]
        return details[0]["streamInfos"][0]["streamingFullURL"]


class AppDelegate(object):
    # Cobbled together from the pycocoa.ObjCSubClass.__doc__,
    # pycocoa.runtime._DeallocObserver and PyObjC examples:
    # <http://taoofmac.com/space/blog/2007/04/22/1745> and
    # <http://stackoverflow.com/questions/24024723/swift-using
    # -nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    # the _Delegate.method(signature) decorator specfies the
    # signature of a Python method in Objective-C type encoding
    # to make the Python method callable from Objective-C.

    # This is rather ugly, especially since the decorator is
    # also required for (private) methods called only from
    # Python, like method .badgelabel, ._rate and ._zoom below.

    # See pycocoa.runtime.split_encoding for type encoding:
    # first is return value, then the method args, no need to
    # include @: for self and the Objective-C selector/cmd.
    @_Delegate.method(b'@' + PyObjectEncoding * 3)
    def init(self, title, app, url):
        self = ObjCInstance(send_super_init(self))

        self.title = title
        self.app = app
        self.player = vlc.MediaPlayer(url)
        self.ratio = 2
        self.scale = 1

        return self

    @_Delegate.method('v@')
    def applicationDidFinishLaunching_(self, notification):
        self.window, view = new_window(title=self.title)
        self.window.setDelegate_(self)
        self.player.set_nsobject(view)

        # Create the main menu.
        menu = NSMenu.alloc().init()
        menu.addItem_(
            new_menu_item(
                'Full Screen', 'enterFullScreenMode:', 'f', ctrl=True
            )
        )

        menu.addItem_(new_menu_seperator())
        menu.addItem_(new_menu_item('Play', 'play:', 'p'))
        menu.addItem_(new_menu_item('Pause', 'pause:', 's'))

        menu.addItem_(new_menu_seperator())
        menu.addItem_(new_menu_item('Faster', 'faster:', '>', shift=True))
        menu.addItem_(new_menu_item('Slower', 'slower:', '<', shift=True))
        menu.addItem_(new_menu_item('Zoom In', 'zoomIn:', '+'))
        menu.addItem_(new_menu_item('Zoom Out', 'zoomOut:', '-'))

        menu.addItem_(new_menu_seperator())
        menu.addItem_(new_menu_item('Close Window', 'windowWillClose:', 'w'))

        menu.addItem_(new_menu_seperator())
        menu.addItem_(new_menu_item('Hide Window', 'hide:', 'h'))
        menu.addItem_(
            new_menu_item(
                'Hide Others', 'hideOtherApplications:', 'h', alt=True
            )
        )
        menu.addItem_(new_menu_item('Show All', 'unhideAllApplications:'))

        menu.addItem_(new_menu_seperator())
        menu.addItem_(new_menu_item('Quit ' + self.title, 'terminate:', 'q'))

        subMenu = NSMenuItem.alloc().init()
        subMenu.setSubmenu_(menu)

        menuBar = NSMenu.alloc().init()
        menuBar.addItem_(subMenu)
        self.app.setMainMenu_(menuBar)

        self.play_(None)

    @_Delegate.method('v@')
    def pause_(self, notification):
        # note, .pause() pauses and un-pauses the video,
        # .stop() stops the video and blanks the window
        if self.player.is_playing():
            self.player.pause()

    @_Delegate.method('v@')
    def play_(self, notification):
        self.player.play()

    @_Delegate.method('v@')
    def windowDidResize_(self, notification):
        if self.window and self.ratio:
            # get and maintain the aspect ratio
            # (the first player.video_get_size()
            #  call returns (0, 0), subsequent
            #  calls return (w, h) correctly)
            w, h = self.player.video_get_size(0)
            r = gcd(w, h)
            if r and w and h:
                r = NSSize_t(w // r, h // r)
                self.window.setContentAspectRatio_(r)
                self.ratio -= 1

    @_Delegate.method('v@')
    def windowWillClose_(self, notification):
        self.app.terminate_(self)

    @_Delegate.method('v@')
    def faster_(self, notification):
        self._rate(2.0)

    @_Delegate.method('v@')
    def slower_(self, notification):
        self._rate(0.5)

    @_Delegate.method(b'v' + PyObjectEncoding)
    def _rate(self, factor):  # called from ObjC method
        r = self.player.get_rate() * factor
        if 0.2 < r < 10.0:
            self.player.set_rate(r)

    @_Delegate.method('v@')
    def zoomIn_(self, notification):
        self._zoom(1.25)

    @_Delegate.method('v@')
    def zoomOut_(self, notification):
        self._zoom(0.80)

    @_Delegate.method(b'v' + PyObjectEncoding)
    def _zoom(self, factor):  # called from ObjC method
        self.scale *= factor
        self.player.video_set_scale(self.scale)


_Delegate = ObjCClass('_Delegate')  # the actual class


def new_menu_item(label, action=None, key='',
                  alt=False, cmd=True, ctrl=False, shift=False):
    # <http://developer.apple.com/documentation/appkit/nsmenuitem/1514858-initwithtitle>
    item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        NSStr(label), get_selector(action), NSStr(key))
    if key:
        mask = 0
        if alt:
            mask |= NSAlternateKeyMask
        if cmd:
            mask |= NSCommandKeyMask
        if ctrl:
            mask |= NSControlKeyMask
        if shift:
            mask |= NSShiftKeyMask  # NSAlphaShiftKeyMask
        if mask:
            item.setKeyEquivalentModifierMask_(mask)
    return item


def new_menu_seperator():
    return NSMenuItem.separatorItem()


def new_window(title, fraction=0.5, low=False):
    frame = NSScreen.alloc().init().mainScreen().frame()
    if 0.1 < fraction < 1.0:
        # use the lower left quarter of the screen size as frame
        w = int(frame.size.width * fraction + 0.5)
        h = int(frame.size.height * w / frame.size.width)
        frame = NSRect4_t(frame.origin.x + 10, frame.origin.y + 10, w, h)

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        NSWindowStyleMaskUsual,  # PYCHOK expected
        NSBackingStoreBuffered,
        False)  # or 0
    window.setTitle_(NSStr(title))

    # create the drawable_nsobject NSView for vlc.py, see
    # vlc.MediaPlayer.set_nsobject() for an alternate NSView object with
    # protocol VLCOpenGLVideoViewEmbedding
    # <http://stackoverflow.com/questions/11562587/create-nsview-directly-from-code>
    # <http://github.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
    view = NSView.alloc().initWithFrame_(frame)
    window.setContentView_(view)
    # force the video/window aspect ratio, adjusted
    # above when the window is/has been resized
    window.setContentAspectRatio_(frame.size)

    window.makeKeyAndOrderFront_(None)
    return window, view


def new_app(title, url):
    app = NSApplication.sharedApplication()
    # pool = NSAutoreleasePool.alloc().init()  # created by NSApplication
    dlg = _Delegate.alloc().init(title, app, url)
    app.setDelegate_(dlg)
    return app


def parse_args():
    parser = argparse.ArgumentParser(
        description='Cisco Video Surveillance Manager Streamer'
    )
    parser.add_argument('--config', '-c', type=str,
                        help='path to config file')
    parser.add_argument('--profile', '-r', type=str,
                        help='profile name to use')
    parser.add_argument('--server', '-s', type=str,
                        help='VSM server address')
    parser.add_argument('--username', '-u', type=str,
                        help='VSM username')
    parser.add_argument('--password', '-p', type=str,
                        help='VSM password')
    parser.add_argument('--stream', '-n', type=int, default=0,
                        help='stream index to display')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.config is None:
        config_file = os.path.expanduser('~/.vsm/credentials')
        exit_without_config = False
    else:
        config_file = args.config
        exit_without_config = True

    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        if args.profile is None:
            args.profile = 'default'
        if args.profile not in config:
            print('Section {} not present in config file {}.'.format(
                args.profile, config_file
            ))
            sys.exit(1)

        cred = config[args.profile]
        if args.server is None:
            args.server = cred.get('server', None)
        if args.username is None:
            args.username = cred.get('username', None)
        if args.password is None:
            args.password = cred.get('password', None)
    elif exit_without_config:
        print('Config file {} does not exist'.format(config_file))
        sys.exit(1)
    else:
        if args.profile is not None:
            print('Argument `profile` must be used only with config files.')
            sys.exit(1)

    if args.server is None:
        print('Mandatory parameter `server` is not specfied.')
        sys.exit(2)
    if args.username is None:
        print('Mandatory parameter `username` is not specfied.')
        sys.exit(2)
    if args.password is None:
        print('Mandatory parameter `password` is not specfied.')
        sys.exit(2)

    session = VSOMSession('https://{}'.format(args.server),
                          username=args.username, password=args.password,
                          verify=False)
    cameras = session.get_cameras()
    streams = {
        name: session.get_stream(uid) for name, uid in cameras.items()
    }
    if args.stream >= len(streams):
        print('Stream index {} is out of bounds. '
              'Only {} streams available.'.format(
                  args.stream, len(streams)))
        sys.exit(1)

    title, url = list(streams.items())[args.stream]
    app = new_app(title, url)
    app.run()


if __name__ == '__main__':
    main()
