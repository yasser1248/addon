// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project', {
	// refresh: function(frm) {
	after_save:function(frm){
		let d2=frm.doc.end_date
	  	let d1=frm.doc.start_date
	   
		frm.doc.period=Math.floor(frappe.datetime.get_diff(d2,d1,'months'))
		// let current_date= frappe.datetime.nowdate()
		// frm.doc.time_untill_project_end=Math.floor(frappe.datetime.get_diff(d2,current_date,'months'))
		// if(frm.doc.time_untill_project_end<0){
		// 	frm.doc.time_untill_project_end="The Time is up"
		// }else if(frm.doc.time_untill_project_end==0){
		// 	frm.doc.time_untill_project_end="Today is last Day"
		// }
		frappe.call({
			method:"pp_addon.tasks.set_time_untill_project_end",
			args:{"period_value":frm.doc.period,"doc_name":frm.doc.name},
			callback:function(r)
			{

				frm.reload_doc()
			}
		})
		
		}
	
	// }
});
// frappe.ui.form.on('Project', {
	

// 	start_date: function(frm) {
// 	  let d2=frm.doc.end_date
// 	  let d1=frm.doc.start_date
// 	  frm.doc.period =Math.floor(frappe.datetime.get_diff(d2,d1)/30);
// 	   frm.refresh_fields('period')	 
// 	},
// 	end_date: function(frm) {
// 	   let d2=frm.doc.end_date
// 	  let d1=frm.doc.start_date
	   
// 	   frm.doc.period =Math.floor(frappe.datetime.get_diff(d2,d1)/30);
// 	   frm.refresh_fields('period')

// 	},
	
	
// });
