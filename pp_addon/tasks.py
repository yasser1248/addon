import frappe
import requests
from datetime import date,datetime
import  math

    
def cron():
    project_list=frappe.db.get_list("Project")
    
    for project in project_list:
        get_project=frappe.get_doc("Project",project.name)
        get_project.time_untill_project_end =(get_project.end_date-date.today())
        
        get_project.time_untill_project_end=get_project.time_untill_project_end.days
    
        if(get_project.time_untill_project_end<0):
            get_project.time_untill_project_end= "The Time is up"
        elif(get_project.time_untill_project_end ==0): 
            get_project.time_untill_project_end="Today is last Day"
            
        get_project.save()
    return True          
def daily():
    project_list=frappe.db.get_list("Project")
    
    for project in project_list:
        get_project=frappe.get_doc("Project",project.name)
        get_project.time_untill_project_end =(get_project.end_date-date.today())
        
        get_project.time_untill_project_end=get_project.time_untill_project_end.days
        # print(f"\n\n\n {project.time_untill_project_end}\n\n\n")
    
        if(get_project.time_untill_project_end<0):
            get_project.time_untill_project_end= "The Time is up"
        elif(get_project.time_untill_project_end ==0):
            get_project.time_untill_project_end="Today is last Day"
            
        get_project.save()
    return True          

@frappe.whitelist()
def set_time_untill_project_end(period_value,doc_name):
    
        get_project=frappe.get_doc("Project",doc_name)
        get_project.period=period_value
        get_project.time_untill_project_end =(get_project.end_date-date.today())
        
        get_project.time_untill_project_end=get_project.time_untill_project_end.days
        # print(f"\n\n\n {project.time_untill_project_end}\n\n\n")
    
        if(get_project.time_untill_project_end<0):
            get_project.time_untill_project_end= "The Time is up"
        elif(get_project.time_untill_project_end ==0):
            get_project.time_untill_project_end="Today is last Day"
            
        get_project.save()
        return True  


def send_report():
    doc = frappe.get_doc("Auto Email Report", "Employees Attendance Details Complete")
    doc.send()
    
    # email_args = {
    #     "message": "Employees Attendance Details Complete",
    #     "recipients": "mohamed.selim@itsystematic.com",
    #     "subject": "Employees Attendance Details Complete",
    # }
    # frappe.enqueue(method=frappe.sendmail, queue="short", timeout=300, now=True ,
    #     **email_args)
    
    # doc.email_to = "mohamed.selim@itsystematic.com"