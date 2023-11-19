// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Projects Meeting', {
	start_meeting: function(frm) {
		let parti=[]
		frm.doc.participate.forEach(part => {
			parti.push(part.participate)
			
			console.log(parti)
		})
		frappe.call({
			method:"pp_addon.api.send_to_participate",
			args:parti,
			callback:function(r){
				console.log(r)
				window.location.href = 'https://addon.newera-soft.com/meeting'
			}
		})
		// window.location.href = 'https://addon.newera-soft.com/meeting'
	},
	// refresh:function(frm){
		
	// }

	send_summary: async function(frm) {
		await frappe.call({
			method: "send_summary",
			doc : frm.doc,
			callback: (r) => {console.log(r);},
		});
	},

	after_save: function(frm) {
		frm.set_df_property("start_meeting", "hidden", 0);
	},
});

