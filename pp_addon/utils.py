import frappe



#recipients is the name who will get message
def send_mail(doc, recipients, msg, title, attachments=None):
    email_args= {
        'recipients':recipients,
        'message':msg,
        'subject':title,
        'reference_doctype':doc.doctype,
        'reference_name':doc.name,
    }
    if attachments:email_args['attachments']=attachments
    frappe.enqueue(method=frappe.sendmail,queue='short',timeout=300,now=True,**email_args)