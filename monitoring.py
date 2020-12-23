#!/usr/bin/env python
import configparser
import datetime
import time
import logging

from modules import odoo
from modules import wifi_lamp

logging.basicConfig(level="INFO")

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
    last_check = datetime.datetime.now()
    while True:
        logging.info("Checking attendances on Odoo")
        # Check if todays' attendance is > supposed daily working time
        time_today = odoo_client.get_total_attendance(period="daily")
        hours_today = time_today.seconds // 3600
        minutes_today = (time_today.seconds // 60) % 60

        if (hours_today >= 7) and (minutes_today >= 42) and not attendance_already_warned_today:
            logging.info("time is up for today")
            wl.green_alert()
            time.sleep(60)
            wl.off()
            attendance_already_warned_today = True
        else:
            logging.info("time not reached yet for today, or already warned (%s)", time_today)

        # check if week attendance is > supposed weekly working time
        time_week = odoo_client.get_total_attendance(period="weekly")
        hours_week = time_week.seconds // 3600
        minutes_week = (time_week.seconds // 60) % 60
        if (hours_week >= 38) and (minutes_week >= 30) and not attendance_already_warned_today:
            logging.info("time is up for this week")
            wl.green_alert()
            time.sleep(60)
            wl.off()
            attendance_already_warned_today = True
        else:
            logging.info("time not reached yet for this week, or already warned (%s)", time_week)

        # check if everything is ok on Grafana

        # Resets counters, if day changed
        if datetime.datetime.now().day != last_check.day:
            attendance_already_warned_today = False
        last_check = datetime.datetime.now()

        # wait a bit before looping again
        time.sleep(60)
        logging.info("Main event loop")
