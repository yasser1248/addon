// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Projects Meeting', {
	start_meeting: function(frm) {
		window.location.href = 'http://192.168.1.10:8059/meeting'
	}
});

