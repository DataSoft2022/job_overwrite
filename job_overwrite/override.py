import frappe
from erpnext.manufacturing.doctype.job_card.job_card import JobCard





class CustomJobCard(JobCard):
    def validate(self):
        self.set_status()
        self.validate_operation_id()
        self.set_sub_operations()
        self.update_sub_operation_status()
        self.validate_work_order()
