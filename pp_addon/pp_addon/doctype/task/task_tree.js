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
                    console.log(nodes[i]);
                    console.log(cur_tree.nodes[nodes[i].value]);
                    c = colors[nodes[i].Status]
                    const node = cur_tree.nodes && cur_tree.nodes[nodes[i].value];
                    if (node.is_root) continue;
                    node.$tree_link.append("<span class='indicator-pill "+ c +" filterable no-indicator-dot ellipsis' style='position: absolute; right: 3%;'>" + nodes[i].Status + "</span>")
                }
            }, 1000);
    }
}
