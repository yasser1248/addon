from . import __version__ as app_version

app_name = "pp_addon"
app_title = "Pp Addon"
app_publisher = "magdyabouelatta"
app_description = "PP Addon"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mabualata1@gmail.com"
app_license = "MIT"

# node_modules
# ____________

node_modules = {
    "frappe-gantt": {
        "js": [
            "assets/pp_addon/node_modules/frappe-gantt/dist/frappe-gantt.min.js",
            "assets/pp_addon/node_modules/frappe-gantt/dist/frappe-gantt.js",
        ],
        "css": [
            "assets/pp_addon/node_modules/frappe-gantt/dist/frappe-gantt.min.css",
        ],
    },
    "dhtmlx-gantt": {
        "js": [
            "assets/pp_addon/node_modules/dhtmlx-gantt/codebase/dhtmlxgantt.js",
        ],
        "css": [
            "assets/pp_addon/node_modules/dhtmlx-gantt/codebase/dhtmlxgantt.css",
        ],
    },
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = node_modules.get("frappe-gantt").get("css") + node_modules.get(
    "dhtmlx-gantt"
).get(
    "css"
)  # "/assets/pp_addon/css/pp_addon.css"
app_include_js = (
    [
        "/assets/pp_addon/js/form.js",
        "/assets/pp_addon/js/gantt_view.js",
        "/assets/pp_addon/js/pp_addon/views/gantt/dhtmlx_gantt_view.js",
        "/assets/pp_addon/js/pp_addon/views/list_factory.js",
    ]
    + node_modules.get("frappe-gantt").get("js")
    + node_modules.get("dhtmlx-gantt").get("js")
)  # "/assets/pp_addon/js/pp_addon.js"

# include js, css files in header of web template
# web_include_css = "/assets/pp_addon/css/pp_addon.css"
# web_include_js = "/assets/pp_addon/js/pp_addon.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pp_addon/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"Task" : "public/js/Task_list.js"}

# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pp_addon.install.before_install"
# after_install = "pp_addon.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pp_addon.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": ["pp_addon.scheduler_tasks.projects_meeting.check_completed_meetings"],
    # "all": ["pp_addon.tasks.custom_time"],
    #  "cron":{
    #     "06 * * * *":["pp_addon.tasks.cron"]
    #  },
    #  "cron":{
    #     "07 * * * *":["pp_addon.tasks.cron"]
    #  },
    "cron": {
        "01 00 * * *": ["pp_addon.tasks.cron"],
        "0 14 * * 4": ["pp_addon.scheduler_tasks.employee_daily_work.send_report"],
        "0 10 * * 0,1,2,3,4": ["pp_addon.scheduler_tasks.employee_checkin_checkout.checkin"],
        "0 18 * * 0,1,2,3,4": ["pp_addon.scheduler_tasks.employee_checkout.check_out", "pp_addon.scheduler_tasks.employee_checkin_checkout.employees_not_done_any_tasks"],
        # "0 0 28,29,30,31 * * ":  ["bash -c '[[ $(date +\%d -d tomorrow) == 01 ]] && bench execute pp_addon.tasks.send_report'"],
    },
    # 	"all": [
    # 		"pp_addon.tasks.all"
    # 	],
    "daily": ["pp_addon.tasks.daily"],
    # 	"hourly": [
    # 		"pp_addon.tasks.hourly"
    # 	],
    # 	"weekly": [
    # 		"pp_addon.tasks.weekly"
    # 	]
    # 	"monthly": [
    # 		"pp_addon.tasks.monthly"
    # 	]
}

# Testing
# -------

# before_tests = "pp_addon.install.before_tests"

# Overriding Methods
# ------------------------------
# override_whitelisted_methods={
# 	"frappe.public.js.frappe.ui.page.add_button":"pp_addon.event.overrides"
# }
override_whitelisted_methods = {
    "frappe.client.validate_link": "pp_addon.override.whitelisted_methods.client.validate_link",
    # 	"frappe.desk.reportview.get": "pp_addon.override.whitelisted_methods.reportview.get",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pp_addon.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {"doctype": "{doctype_4}"},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pp_addon.auth.validate"
# ]
fixtures = [
    {
        "dt": ("Property Setter"),
        "filters": [
            ["doc_type", "in", ("Kanban Board")],
            ["field_name", "in", ("kanban_board_name",)],
        ],
    },
    {"dt": ("Kanban Board"), "filters": [["kanban_board_name", "in", ("Task")]]},
    {
        "dt": "Role",
        "filters": [
            ["name", "in", ("Addon Manager", "Addon User", "Addon Limited")],
        ],
    },
    {
        "dt": ("Custom Field"),
        "filters": [["dt", "in", ("Employee",)], ["fieldname", "in", ("custom_employee_signature")]],
    },
    # "Lead Source",
    # {
    #     "dt": ("Print Format"),
    #     "filters": [
    #         ["name" , "in" , ("")]],
    # },
]

calendars = [
    "Task",
]

# To ignore links to specific DocTypes when deleting documents
# ignore_links_on_delete
# ------------------------------------------------------------

doctypes = [
    "Department",
    "Standard Item",
    "Standards Group",
    "Standards",
    "Employee",
    "Organization",
    "Projects Meeting",
    "Task",
    "Projects Meeting Desction",
    "Vendor",
    "Project items",
    "Projects Objectives",
    "Vend employee",
    "Projects charter",
    "Project Sponsors",
    "Projects Objectives Child",
    "Project",
    "Project payment",
    "Stakholder",
    "Kick of Meeting Documents",
    "pp1",
    "Projects Tender",
    "Project close",
    "Project close child",
    "Project Qtable",
    "Project stakholder",
    "Project Phase",
    "Projects Risks child",
    "Project Risk type",
    "Project learn child3",
    "Project learn child2",
    "Task type",
    "Actions",
    "Transaction child",
    "Project Document Type",
    "Stakholder Role",
    "Performance type",
    "Item type",
    "Project status",
    "Position",
    "Project Catogery",
    "Project learning lesson",
    "Project learn child4",
    "Project learn child1",
    "Project team asses",
    "Project change",
    "Projects Achievement scene",
    "Type of asses",
    "project team ass child",
    "Project Meeting Participate",
    "Projects Meeting Melement",
    "Project quality",
    "Projects Bidding",
    "Projects Deliverable",
    "Projects study",
    "Projects Risks",
    "Projects Milestone",
    "Projects Milestone child",
    "Project quality rules",
    "Project labor",
    "Project change approve",
    "Tender company",
    "Project Document Child",
    "Project Document",
    "Dependent task",
    "Project quality metrices",
    "Project payment child",
    "Transaction",
    "Project qty",
    "Project child",
    "Service",
    "PP_Project milestone",
    "Transaction type",
    "Deliverable child",
    "Project change child",
]
ignore_links_on_delete = doctypes

# Custom Hook
# Cascading deletion for specified doctypes
# -----------------------------------------

cascading_deletion_doctypes = doctypes

# login

after_login = "pp_addon.login.login.after_login"
