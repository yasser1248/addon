// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

// frappe.listview.on('Task', {
// 	refresh:function(frm) {
// 		console.log("Heloo")
// 		frm.add_custom_button(__("Clear Error Logs"), function() {
// 			console.log("hello")
// 		})
// 		// listview.page.add_menu_item(("Show M"), function () {console.log("hello Escanoor")
// 		listview.add_action_item(("Show M"), function () {console.log("hello Escanoor")
// 		console.log("bye")
// 	},"Test")
// },


// });


// frappe.listview_settings['Task'] = {
//     button: {
//         show: function(doc) {
//             return true;
//         },
//         get_label: function() {
//             return __('View');
//         },
//         get_description: function(doc) {
//             return __('Open {0}', [doc.name])
//         },
//         action: function(doc) {
//             //frappe.set_route("/app/print/Purchase Order/" + doc.name);
//             console.log("hello2")
//             var objWindowOpenResult = window.open(frappe.urllib.get_full_url("/printview?"
//               + "doctype=" + encodeURIComponent("Task")
//               + "&name=" + encodeURIComponent(doc.name)
//               + "&trigger_print=0"
//               + "&format=General"
//               + "&no_letterhead=0"
//               + "&_lang=tr"
//             ));

//             if(!objWindowOpenResult) {
//                 console.log("hello2")
//                 msgprint(__("Please set permission for pop-up windows in your browser!")); return;

//             }
//         }
//     }
// }


frappe.listview_settings['Task'] = {
   onload: function(list) {
	   list.page.add_button("Show ME", function() {
        window.open("http://192.168.1.10:8059/test");
	   },"test");
   },
};