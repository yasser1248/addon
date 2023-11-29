
frappe.views.ListFactory = class ListFactory extends frappe.views.ListFactory {
	make(route) {
		const me = this;
		const doctype = route[1];

        // override
        if (doctype == "Task" && route[2] == "Gantt") {
            var view_name = "DHTMLXGantt"
        }

		else {
			// List / Gantt / Kanban / etc
			var view_name = frappe.utils.to_title_case(route[2] || "List");
		}

		// File is a special view
		if (doctype == "File" && !["Report", "Dashboard"].includes(view_name)) {
			view_name = "File";
		}

		let view_class = frappe.views[view_name + "View"];
		if (!view_class) view_class = frappe.views.ListView;

		if (view_class && view_class.load_last_view && view_class.load_last_view()) {
			// view can have custom routing logic
			return;
		}

		frappe.provide("frappe.views.list_view." + doctype);

		frappe.views.list_view[me.page_name] = new view_class({
			doctype: doctype,
			parent: me.make_page(true, me.page_name),
		});

		me.set_cur_list();
	}
};
