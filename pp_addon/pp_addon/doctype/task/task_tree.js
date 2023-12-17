frappe.treeview_settings['Task'] = {
    breadcrumb: 'Task',
    title: 'Chart of Tasks',
    filters: [
        {
            fieldname: 'project',
            fieldtype:'Link',
            options: 'Project',
            label: 'Project',
        }
    ],
    get_tree_nodes: 'pp_addon.pp_addon.doctype.task.task.get_children',
    add_tree_node: 'pp_addon.pp_addon.doctype.task.task.add_node',
    // fields for a new node
    fields: [
        {
            fieldtype: 'Check', fieldname: 'is_group', label: 'Is Group',
            description: 'Further nodes can be only created under \'Group\' type nodes'
        },
        {
            fieldtype: 'Link', fieldname: 'project',
            label: 'Project', options: 'Project'
        },
        {
            fieldtype: 'Data', fieldname: 'subject',
            label: 'Subject', reqd: true
        },
    ],
    on_get_node: function(nodes) {
        // triggered when `get_tree_nodes` returns nodes
            setTimeout(() => {
                var colors = {
                    "Open": "orange",
                    "Overdue": "red",
                    "Pending Review": "orange",
                    "Working": "orange",
                    "Completed": "green",
                    "Cancelled": "dark grey",
                    "Template": "blue"
                };
                for(let i=0; i<nodes.length; i++) {
                    c = colors[nodes[i].Status]
                    const node = cur_tree.nodes && cur_tree.nodes[nodes[i].value];
                    if (node.is_root) continue;
                    node.$tree_link.append("<span class='indicator-pill "+ c +" filterable no-indicator-dot ellipsis' style='position: absolute; right: 3%;'>" + nodes[i].Status + "</span>")
                }
            }, 1000);
    },

    // enable custom buttons beside each node
    extend_toolbar: true,
    // custom buttons to be displayed beside each node
    toolbar: [
        {
            label: 'Edit',
            condition: function (node) {if (node.is_root == undefined) return true;},
            click: function (node, btn) {click_edit_node(node, btn);},
            btnClass: 'hidden-xs'
        }
    ]
}

function click_edit_node(node, btn) {
    frappe.call({
        // GET Task doc for node
        method: "frappe.client.get",
        type: "GET",
        args: { doctype: "Task", name: node.label, filters: null },
        callback: (r) => {
            if (Object.keys(r.message).length > 0) {
                // Create the Dialog
                let d = new frappe.ui.Dialog({
                    title: r.message.name,
                    fields: get_fields(r.message),
                    size: 'small', // small, large, extra-large 
                    primary_action_label: 'Save',
                    async primary_action(values) {
                        if (values.description) delete values.description;
                        values["doctype"] = "Task";
                        values["name"] = node.label;
                        values["description"] = cur_dialog.get_value("description");
                        const getDifference = (a, b) =>
                            Object.entries(b).filter(([key, val]) => a[key] !== val && key in a).reduce((a, [key, v]) => ({ ...a, [key]: v }), {});
                        const c = getDifference(r.message, values);
                        await frappe.call({
                            method: "frappe.client.set_value",
                            args: {
                                doctype: "Task",
                                name: node.label,
                                fieldname: c,
                            },
                            callback: function (r) {
                                console.log(r.message);
                            },
                        });
                        d.hide();
                    }
                });
                d.show();
                setTimeout(() => {
                    dragElement(document.getElementsByClassName("modal-content")[0]);
                }, 1 * 1000);
            }
        },
        error: (r) => {console.log(r);},
    })
}

function get_fields(doc) {
    let fields = frappe.get_meta("Task").fields;
    fields = fields.filter((e) => { if (!in_list(["sb_depends_on", "depends_on", "depends_on_tasks"], e.fieldname)) return e;});
    fields.forEach(element => {
        if (doc[element.fieldname] != undefined || doc[element.fieldname] != null) {
            element["default"] = doc[element.fieldname];
        }
    });
    return fields
}

function dragElement(elmnt) {
    var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
    if (document.getElementsByClassName("modal-header")[0]) {
        // if present, the header is where you move the DIV from:
        document.getElementsByClassName("modal-header")[0].onmousedown = dragMouseDown;
    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = elmnt.offsetTop - pos2 + "px";
        elmnt.style.left = elmnt.offsetLeft - pos1 + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
