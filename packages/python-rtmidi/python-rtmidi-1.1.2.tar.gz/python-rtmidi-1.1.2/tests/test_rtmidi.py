#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for the rtmidi module."""

import time
import unittest

import rtmidi


class RtMidiTestCase(unittest.TestCase):

    NOTE_ON = [0x90, 48, 100]
    NOTE_OFF = [0x80, 48, 16]
    TEST_PORT_NAME = 'rtmidi test'
    DELAY = 0.1

    def setUp(self):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()

        # TODO: find better solution than this hack-ish strategy to find out
        # the port number of the virtual output port, which we have to use,
        # because for ALSA virtual ports, their name includes the client id.
        # See: https://github.com/thestk/rtmidi/issues/88
        ports_before = self.midi_in.get_ports()
        self.midi_out.open_virtual_port()
        ports_after = self.midi_in.get_ports()
        port_name = list(set(ports_after).difference(ports_before))[0]

        for portnum, port in enumerate(ports_after):
            if port == port_name:
                self.midi_in.open_port(portnum)
                break
        else:
            raise IOError("Could not find MIDI output port.")

    def tearDown(self):
        self.midi_in.close_port()
        del self.midi_in
        self.midi_out.close_port()
        del self.midi_out

    def test_is_port_open(self):
        assert self.midi_in.is_port_open()
        self.midi_in.close_port()
        assert not self.midi_in.is_port_open()

        # virtual ports can't be closed
        assert self.midi_out.is_port_open()
        self.midi_out.close_port()
        assert self.midi_out.is_port_open()

        midi_out2 = rtmidi.MidiOut()
        assert not midi_out2.is_port_open()
        midi_out2.open_virtual_port()
        assert midi_out2.is_port_open()
        del midi_out2

    def test_send_and_get_message(self):
        self.midi_out.send_message(self.NOTE_ON)
        self.midi_out.send_message(self.NOTE_OFF)
        time.sleep(self.DELAY)
        message_1, _ = self.midi_in.get_message()
        message_2, _ = self.midi_in.get_message()
        self.assertEqual(message_1, self.NOTE_ON)
        self.assertEqual(message_2, self.NOTE_OFF)

    def test_callback(self):
        messages = []

        def callback(event, data):
            messages.append((event[0], data))

        self.midi_in.set_callback(callback, data=42)
        self.midi_out.send_message(self.NOTE_ON)
        self.midi_out.send_message(self.NOTE_OFF)
        time.sleep(self.DELAY)
        self.assertEqual(messages[0], (self.NOTE_ON, 42))
        self.assertEqual(messages[1], (self.NOTE_OFF, 42))

        self.midi_in.cancel_callback()
        messages = []
        self.midi_out.send_message(self.NOTE_ON)
        self.midi_out.send_message(self.NOTE_OFF)
        time.sleep(self.DELAY)
        self.assertEqual(messages, [])


if __name__ == '__main__':
    unittest.main()
