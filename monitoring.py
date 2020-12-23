#!/usr/bin/env python
import configparser
import datetime
import time

from modules import odoo
from modules import wifi_lamp

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("wifi_lamp.ini")
    wl = wifi_lamp.wifi_lamp(config['wifi']['ip_address'])
    odoo_client = odoo.odoo(config['odoo']['address'],
                            config['odoo']['port'],
                            config['odoo']['database'],
                            config['odoo']['username'],
                            config['odoo']['password'])

    attendance_already_warned_today = False
    last_check = datetime.now()
    while True:
        # Check if todays' attendance is > supposed daily working time
        time_today = odoo_client.get_total_attendance(period="daily")
        hours_today = time_today.seconds // 3600
        minutes_today = (time_today.seconds // 60) % 60

        if (hours_today >= 7) and (minutes_today >= 42) and not attendance_already_warned_today:
            wl.green_alert()
            time.sleep(60)
            wl.off()
            attendance_already_warned_today = True

        # check if week attendance is > supposed weekly working time
        time_today = odoo_client.get_total_attendance(period="weekly")
        hours_today = time_today.seconds // 3600
        minutes_today = (time_today.seconds // 60) % 60
        if (hours_today >= 38) and (minutes_today >= 30) and not attendance_already_warned_today:
            wl.green_alert()
            time.sleep(60)
            wl.off()
            attendance_already_warned_today = True

        # check if everything is ok on Grafana

        # Resets counters, if day changed
        if datetime.now().day != last_check.day:
            attendance_already_warned_today = False
        last_check = datetime.now()

        # wait a bit before looping again
        time.sleep(60)
