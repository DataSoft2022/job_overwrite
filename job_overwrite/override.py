import frappe
from erpnext.manufacturing.doctype.job_card.job_card import JobCard
from frappe.utils.data import flt, get_datetime, time_diff_in_hours





class CustomJobCard(JobCard):
    def validate(self):
        self.set_status()
        self.validate_time_logs()
        self.validate_operation_id()
        self.set_sub_operations()
        self.update_sub_operation_status()
        self.validate_work_order()


    

    def validate_time_logs(self):
        self.total_time_in_mins = 0.0
        self.total_completed_qty = 0.0

        if self.get("time_logs"):
            for d in self.get("time_logs"):
                if d.to_time and get_datetime(d.from_time) > get_datetime(d.to_time):
                    frappe.throw(_("Row {0}: From time must be less than to time").format(d.idx))

                if d.from_time and d.to_time:
                    d.time_in_mins = time_diff_in_hours(d.to_time, d.from_time) * 60
                    self.total_time_in_mins += d.time_in_mins
                

                if d.completed_qty and not self.sub_operations:
                    self.total_completed_qty += d.completed_qty

            self.total_completed_qty = flt(self.total_completed_qty, self.precision("total_completed_qty"))

        for row in self.sub_operations:
            self.total_completed_qty += row.completed_qty
