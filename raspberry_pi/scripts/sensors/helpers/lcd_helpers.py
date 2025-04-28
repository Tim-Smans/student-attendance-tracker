#!/usr/bin/env python3

from time import sleep
import smbus
import RPi.GPIO as GPIO




class LCDScreen:
    def __init__(self):
        rev = GPIO.RPI_REVISION
        if rev == 2 or rev == 3:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = smbus.SMBus(0)

        self.DISPLAY_TEXT_ADDR = 0x3e 



    def set_text(self, text):
        self.text_cmd(0x01) 
        sleep(.05)
        self.text_cmd(0x08 | 0x04)  # Display on, no cursor
        self.text_cmd(0x28)  # 2-line mode
        sleep(.05)

        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.text_cmd(0xc0)
                if c == '\n':
                    continue
            count += 1

            if not self.safe_write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c)):
                print("LCD not connected!")
                break
            
    def set_text_norefresh(self, text):
        self.text_cmd(0x02)  # Return home
        sleep(.05)
        self.text_cmd(0x08 | 0x04)
        self.text_cmd(0x28)
        sleep(.05)

        count = 0
        row = 0
        while len(text) < 32:
            text += ' '
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.text_cmd(0xc0)
                if c == '\n':
                    continue
            count += 1

            if not self.safe_write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c)):
                print("LCD not connected!")
                break

    def text_cmd(self, cmd):
        if not self.safe_write_byte_data(self.DISPLAY_TEXT_ADDR, 0x80, cmd):
            print("LCD not connected!")

    def set_cursor(self, row):
        addr = 0x80 if row == 0 else 0xC0
        self.text_cmd(addr)

    def clear(self):
        self.text_cmd(0x01)
        sleep(0.05)

    def write(self, text):
        for c in text:
            if not self.safe_write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c)):
                print("LCD not connected!")
                break
            
    def scroll_line(self, line, message, delay=0.3):
        
        padding = " " * 16
        
        message = padding + message + padding
        for i in range(len(message) - 15):
            self.set_cursor(line)
            self.write(message[i:i+16])
            sleep(delay)

    def safe_write_byte_data(self, addr, cmd, val):
        try:
            self.bus.write_byte_data(addr, cmd, val)
            return True
        except (OSError, IOError):
            return False

