import frappe
from pp_addon.utils import send_mail


@frappe.whitelist()
def send_to_participate(**args):
    for  key,value in args.items():
        if key!="cmd":
            doc=frappe.get_doc("Stakholder",value)
            # msg=f"To: {doc.name} <br> Invite for meeting <br> <a href='https://addon.newera-soft.com/meeting'>Press Here for Meeting</a>"
            msg = f"""
                To: {doc.name}
                Invite for meeting
                <a href='https://addon.newera-soft.com/meeting'>Press Here for Meeting</a>
                https://addon.newera-soft.com/meeting
            """
            send_mail( doc,doc.email,msg=msg,title="Project Meeting")
    return "Meeting Link sent to participate members"