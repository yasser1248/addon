// Copyright (c) 2024, magdyabouelatta and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Project Expenses", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Project Expenses Details", {
    expenses_remove(frm, cdt, cdn) {
        if (frm.doc.expenses.length > 0) {
            frm.doc.totals = 0;
            for (let i=0; i< frm.doc.expenses.length; i++) {
                frm.set_value("totals", frm.doc.totals + frm.doc.expenses[i].amount);
            }
            frm.refresh_field("totals");
        }
        else { frm.set_value("totals", 0); frm.refresh_field("totals"); }
    },
    amount(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frm.set_value("totals", frm.doc.totals + row.amount);
        frm.refresh_field("totals");
    },
});
