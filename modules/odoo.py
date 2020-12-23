import datetime
from datetime import date, timedelta, datetime

import odoorpc
import pytz


class odoo:

    def __init__(self, odoo_addr, odoo_port, odoo_db, odoo_user, odoo_password):
        self.login = odoo_user
        self.password = odoo_password
        self.odoo_db = odoo_db
        self.odoo_addr = odoo_addr
        self.odoo_port = odoo_port
        self.handle = odoorpc.ODOO(host=self.odoo_addr, port=self.odoo_port, protocol="jsonrpc+ssl")
        self.handle.login(self.odoo_db, self.login, self.password)
        # Search oneself to get the res.users.id, then the hr.employee.id
        self.user_id = self.handle.execute('res.users', 'search', [('login', '=', self.login)])[0]
        self.employee_id = self.handle.execute('res.users', 'read',
                                               self.user_id, ['employee_ids'])[0]['employee_ids'][0]

    def get_total_attendance(self, period="daily"):
        if period == "daily":
            begin_midnight = "{}T00:00:00.0Z".format(date.today())
            end_midnight = "{}T00:00:00.0Z".format(date.today() + timedelta(days=1))
        else:
            today = date.today()
            last_monday = today - timedelta(days=today.weekday())
            begin_midnight = "{}T00:00:00.0Z".format(last_monday)
            coming_monday = today + timedelta(days=-today.weekday(), weeks=1)
            end_midnight = "{}T00:00:00.0Z".format(coming_monday)

        attendances_ids = self.handle.execute('hr.attendance', 'search',
                                              [('employee_id', '=', self.employee_id),
                                               ("check_in", ">=", begin_midnight),
                                               ("check_in", "<", end_midnight)
                                               ])
        attendances_details = self.handle.execute('hr.attendance', 'read', attendances_ids)
        total_time_today = 0
        for i in attendances_details:
            checkin = i['check_in']  # str '2020-12-22 15:44:11' /!\ in GMT
            checkout = i['check_out'] if i['check_out'] is not False else \
                datetime.datetime.strftime(datetime.datetime.now(pytz.UTC), "%Y-%m-%d %H:%M:%S")

            checkin_dt = datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
            checkout_dt = datetime.strptime(checkout, '%Y-%m-%d %H:%M:%S')
            total_time_today += (checkout_dt - checkin_dt).total_seconds()
        return timedelta(seconds=total_time_today)
