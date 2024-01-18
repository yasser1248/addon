// Copyright (c) 2024, magdyabouelatta and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Project Expenses", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Project Expenses Details", {
    debit(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.debit) {
            row.balance = row.debit - row.credit;
            frm.refresh_field("expenses");
        }
    },

    credit(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.credit) {
            row.balance = row.debit - row.credit;
            frm.refresh_field("expenses");
        }
    },
});
