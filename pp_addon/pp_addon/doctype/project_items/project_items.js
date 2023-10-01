// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt
frappe.ui.form.on('PP_Qtable', {
	

	qty: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.deliver_value = flt(row.deliver) * flt(row.unit_price);
		row.balance = flt(row.qty) * flt(row.unit_price) - row.deliver_value;
		if (flt(row.qty) < flt(row.deliver) ) { frappe.throw(' Deliver must be equal or less than qty' )}
		let sum =0;
		var d = locals[cdt][cdn];
		frm.doc.items.forEach(function (d) {
			sum += flt(d.deliver_value);

		}
	);//end for each
	if (sum > flt(frm.doc.project_budget)) {frappe.throw('must be equal or less than Project Budget' )}
		frm.set_value("project_balance", flt(frm.doc.project_budget)-flt(sum));
		frm.refresh_fields("balance");
		frm.refresh_fields("deliver_value");


	},
	unit_price: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.deliver_value = flt(row.deliver) * flt(row.unit_price);
		row.balance = flt(row.qty) * flt(row.unit_price) - row.deliver_value;
		frm.doc.project_balance = flt(row.balance);
		
		let sum = 0;
		var d = locals[cdt][cdn];
		frm.doc.items.forEach(function (d) {
			sum += flt(d.deliver_value);

		}

		);//end for each

		if (sum > flt(frm.doc.project_budget)) {frappe.throw(' must be equal or less than Project Budget' )}
		frm.set_value("project_balance", flt(frm.doc.project_budget)-flt(sum));
		frm.refresh_fields("balance");
		frm.refresh_fields("deliver_value");
	},

	deliver: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		row.deliver_value = flt(row.deliver) * flt(row.unit_price);
		row.balance = flt(row.qty) * flt(row.unit_price) - row.deliver_value;
		if (flt(row.qty) < flt(row.deliver) ) { frappe.throw(' Deliver must be equal or less than qty' )}
		let sum =0;
		var d = locals[cdt][cdn];
		frm.doc.items.forEach(function (d) {
			sum += flt(d.deliver_value);

		}

		);//end for each

		if (sum > flt(frm.doc.project_budget)) {frappe.throw(' must be equal or less than Project Budget' )}
		frm.set_value("project_balance", flt(frm.doc.project_budget)-flt(sum));
		
		frm.refresh_fields("balance");
		frm.refresh_fields("deliver_value");

	}


});

