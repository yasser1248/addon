frappe.provide("frappe.views");

frappe.flags.callServer = false;

frappe.views.DHTMLXGanttView = class DHTMLXGanttView extends frappe.views.ListView {
	get view_name() {
		return "DHTMLX Gantt";
	}

	setup_defaults() {
		return super.setup_defaults().then(() => {
			this.page_title = this.page_title + " " + __("Gantt");
			this.calendar_settings = frappe.views.calendar[this.doctype] || {};

			if (typeof this.calendar_settings.gantt == "object") {
				Object.assign(this.calendar_settings, this.calendar_settings.gantt);
			}

			if (this.calendar_settings.order_by) {
				this.sort_by = this.calendar_settings.order_by;
				this.sort_order = "asc";
			} else {
				this.sort_by =
					this.view_user_settings.sort_by || this.calendar_settings.field_map.start;
				this.sort_order = this.view_user_settings.sort_order || "asc";
			}

			this.fields.push(["project", "Task"]);
			this.fields.push(["exp_start_date", "Task"]);
			this.fields.push(["exp_end_date", "Task"]);
			this.fields.push(["is_milestone", "Task"]);
			this.fields.push(["progress", "Task"]);
			this.fields.push(["parent_task", "Task"]);
			this.fields.push(["task", "Dependent task"]);
		});
	}

	setup_view() {}

	prepare_data(data) {
		super.prepare_data(data);
		this.prepare_tasks();
	}

	prepare_tasks() {
		var me = this;
		var meta = this.meta;
		var field_map = this.calendar_settings.field_map;

		this.tasks = this.data.map(function (item) {
			// set progress
			var progress = 0;
			if (field_map.progress && $.isFunction(field_map.progress)) {
				progress = field_map.progress(item);
			} else if (field_map.progress) {
				progress = item[field_map.progress] / 100;
			}

			// title
			var label;
			if (meta.title_field) {
				label = item.progress
					? __("{0} ({1}) - {2}%", [item[meta.title_field], item.name, item.progress])
					: __("{0} ({1})", [item[meta.title_field], item.name]);
			} else {
				label = item[field_map.title];
			}

			var r = {
				start_date: item[field_map.start],
				duration: frappe.datetime.get_day_diff(item[field_map.end], item[field_map.start]),
				text: label,
				id: item[field_map.id || "name"],
				doctype: me.doctype,
				progress: progress,
				parent: item["parent_task"] ? item["parent_task"] : 0,
			};

			if (item.color && frappe.ui.color.validate_hex(item.color)) {
				r["custom_class"] = "color-" + item.color.substr(1);
			}

			if (item.is_milestone) {
				r["custom_class"] = "bar-milestone";
			}

			return r;
		});

		this.links = this.data.map(function (item, index) {
			if (item.task) {
				return {
					id: `${item[field_map.id || "name"]}`,
					source: item.task.split(" "),
					target: item[field_map.id || "name"],
					type: 0,
				};
			}
			return;
		});
		this.links = this.links.filter(function (element) {
			return element !== undefined;
		});
	}

	render() {
		this.load_lib.then(() => {
			this.render_gantt();
		});
	}

	render_header() {

	}

	render_gantt() {
		const me = this;
		const gantt_view_mode = this.view_user_settings.gantt_view_mode || "Day";
		const field_map = this.calendar_settings.field_map;
		const date_format = "%Y-%m-%d ";

		this.toggle_side_bar();
		this.$result.empty();
		this.$result.addClass("gantt-modern");
		this.$result.attr("id", "gantt-modern");
		// this.$result.attr("style", "width:100%; height:100vh;");

		// initialize gantt
		// gantt.config.fit_tasks = true; 
		gantt.config.date_format = date_format;
		gantt.init("gantt-modern");
		gantt.parse({
			data: this.tasks,
			links: this.links,
		});

		// Events
		gantt.attachEvent("onAfterTaskDrag", function(id, mode, e){
			// Checks
			if (!me.can_write) return;
			// Handle multiple events
			if (frappe.flags.callServer === false) {
				frappe.flags.callServer = true;
			}
			else {
				return;
			}

			const task = me.tasks.find((e) => {return e.id === id});
			if (in_list(["resize", "move"], mode)) {
				frappe.db.set_value(task.doctype, task.id, {
					[field_map.start]: frappe.datetime.obj_to_str(task.start_date),
					[field_map.end]: frappe.datetime.obj_to_str(task.end_date),
				}).then((r) => {
					console.log(r.message);
					frappe.flags.callServer = false;
				});
			}
			else if (mode === "progress") {
				frappe.db.set_value(task.doctype, task.id, {
					progress: Math.floor(task.progress * 100),
				}).then((r) => {
					console.log(r.message);
					frappe.flags.callServer = false;
				});
			}
		});

		gantt.attachEvent("onAfterLinkAdd", function(id,item){
			// Checks
			if (!me.can_write) return;
			// Handle multiple events
			if (frappe.flags.callServer === false) {
				frappe.flags.callServer = true;
			}
			else {
				return;
			}

			const doctype = (me.tasks.find((e) => {return e.id === item.target})).doctype;
			// Add new child depends_on
			frappe.call({
				method: "pp_addon.public.js.pp_addon.views.gantt.gantt_apis.on_afte_link_add",
				args: { doctype: doctype, link: item,},
				callback: (r) => {
					console.log(r.message);
					frappe.flags.callServer = false;
				},
				error: (r) => { console.log(r); },
			})
		});

		gantt.attachEvent("onAfterTaskAdd", function(id,item){
			// Checks
			if (!me.can_write) return;
			// Handle multiple events
			if (frappe.flags.callServer === false) {
				frappe.flags.callServer = true;
			}
			else {
				return;
			}

			const doctype = me.doctype;
			frappe.call({
				method: "pp_addon.public.js.pp_addon.views.gantt.gantt_apis.on_after_task_add",
				args: { doctype: doctype, item: item },
				callback: (r) => {
					if (Object.keys(r.message).length > 0) {
						console.log(r.message);
						frappe.flags.callServer = false;
						item.id = r.message.name;
						this.tasks.push(item);
						gantt.refreshData();
					}
				},
				error: (r) => { console.log(r.message) },
			});
		});

		gantt.attachEvent("onAfterTaskUpdate", function(id,item){
			// Checks
			if (!me.can_write) return;
			// Handle multiple events
			if (frappe.flags.callServer === false) {
				frappe.flags.callServer = true;
			}
			else {
				return;
			}

			frappe.call({
				method: "pp_addon.public.js.pp_addon.views.gantt.gantt_apis.on_after_task_update",
				args: { doctype: me.doctype, item: item, id: id, },
				callback: (r) => {
					if (Object.keys(r.message).length > 0) {
						console.log(r.message);
						frappe.flags.callServer = false;
					}
				},
				error: (r) => { console.log(r.message); }
			});
		});

		// this.setup_view_mode_buttons();
		// this.set_colors();
	}

	setup_view_mode_buttons() {
		// view modes (for translation) __("Day"), __("Week"), __("Month"),
		//__("Half Day"), __("Quarter Day")

		let $btn_group = this.$paging_area.find(".gantt-view-mode");
		if ($btn_group.length > 0) return;

		const view_modes = this.gantt.options.view_modes || [];
		const active_class = (view_mode) => (this.gantt.view_is(view_mode) ? "btn-info" : "");
		const html = `<div class="btn-group gantt-view-mode">
				${view_modes
					.map(
						(value) => `<button type="button"
						class="btn btn-default btn-sm btn-view-mode ${active_class(value)}"
						data-value="${value}">
						${__(value)}
					</button>`
					)
					.join("")}
			</div>`;

		this.$paging_area.find(".level-left").append(html);

		// change view mode asynchronously
		const change_view_mode = (value) =>
			setTimeout(() => this.gantt.change_view_mode(value), 0);

		this.$paging_area.on("click", ".btn-view-mode", (e) => {
			const $btn = $(e.currentTarget);
			this.$paging_area.find(".btn-view-mode").removeClass("btn-info");
			$btn.addClass("btn-info");

			const value = $btn.data().value;
			change_view_mode(value);
		});
	}

	set_colors() {
		const classes = this.tasks
			.map((t) => t.custom_class)
			.filter((c) => c && c.startsWith("color-"));

		let style = classes
			.map((c) => {
				const class_name = c.replace("#", "");
				const bar_color = "#" + c.substr(6);
				const progress_color = frappe.ui.color.get_contrast_color(bar_color);
				return `
				.gantt .bar-wrapper.${class_name} .bar {
					fill: ${bar_color};
				}
				.gantt .bar-wrapper.${class_name} .bar-progress {
					fill: ${progress_color};
				}
			`;
			})
			.join("");

		style = `<style>${style}</style>`;
		this.$result.prepend(style);
	}

	get_item(name) {
		return this.data.find((item) => item.name === name);
	}

	get required_libs() {
		return [
			"assets/pp_addon/node_modules/dhtmlx-gantt/codebase/dhtmlxgantt.css",
			"assets/pp_addon/node_modules/dhtmlx-gantt/codebase/dhtmlxgantt.js",
		];
	}
};

// this.gantt = new Gantt(this.$result[0], this.tasks, {
// 	bar_height: 35,
// 	bar_corner_radius: 4,
// 	resize_handle_width: 8,
// 	resize_handle_height: 28,
// 	resize_handle_corner_radius: 3,
// 	resize_handle_offset: 4,
// 	view_mode: gantt_view_mode,
// 	date_format: "YYYY-MM-DD",
// 	on_click: (task) => {
// 		frappe.set_route("Form", task.doctype, task.id);
// 	},
// 	on_date_change: (task, start, end) => {
// 		if (!me.can_write) return;
// 		frappe.db.set_value(task.doctype, task.id, {
// 			[field_map.start]: moment(start).format(date_format),
// 			[field_map.end]: moment(end).format(date_format),
// 		});
// 	},
// 	on_progress_change: (task, progress) => {
// 		if (!me.can_write) return;
// 		var progress_fieldname = "progress";

// 		if ($.isFunction(field_map.progress)) {
// 			progress_fieldname = null;
// 		} else if (field_map.progress) {
// 			progress_fieldname = field_map.progress;
// 		}

// 		if (progress_fieldname) {
// 			frappe.db.set_value(task.doctype, task.id, {
// 				[progress_fieldname]: parseInt(progress),
// 			});
// 		}
// 	},
// 	on_view_change: (mode) => {
// 		// save view mode
// 		me.save_view_user_settings({
// 			gantt_view_mode: mode,
// 		});
// 	},
// 	custom_popup_html: (task) => {
// 		var item = me.get_item(task.id);

// 		var html = `<div class="title">${task.name}</div>
// 			<div class="subtitle">${moment(task._start).format("MMM D")} - ${moment(task._end).format(
// 			"MMM D"
// 		)}</div>`;

// 		// custom html in doctype settings
// 		var custom = me.settings.gantt_custom_popup_html;
// 		if (custom && $.isFunction(custom)) {
// 			var ganttobj = task;
// 			html = custom(ganttobj, item);
// 		}
// 		return '<div class="details-container">' + html + "</div>";
// 	},
// });