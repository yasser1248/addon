// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Projects Meeting', {
	refresh: function(frm) {
		if (!frm.is_new() && !frm.doc.invitation_sent) {
			frm.add_custom_button(__("Send Invitation"), function() {
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
						if (r.message) {
							frappe.show_alert({message: __(r.message), indicator: "green",});
							frm.set_value("invitation_sent", 1);
							// remove custom button
							frm.remove_custom_button('Send Invitation');
							frm.save();
						}
				}
			})
			}).css({ 'background-color': '#25D366', 'color': 'white' });
		}
		if (frm.doc.invitation_sent) {
			frm.add_custom_button(__("Start Meeting"), function() {
				frm.trigger("start_meeting")
			}).css({ 'background-color': '#25c7d3', 'color': 'white' });
		}
	},

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

	// after_save: function(frm) {
	// 	frm.set_df_property("start_meeting", "hidden", 0);
	// },
});

