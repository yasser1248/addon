
frappe.ui.form.Form = class FrappeForm extends frappe.ui.form.Form {
    setup() {
        super.setup();
        console.log("Form -> ");
        console.log(this);
        const h = 1080;
        const w = 1920;
        if ((window.innerHeight / window.innerWidth) > (h / w) && !isMobileDevice()) {
            this.layout_main.addEventListener("change", async(event) => {
                console.log("event -> ");
                console.log(event);
                if (this.is_new() && check_mandatory(this)) {
                    try {
                        this.save();
                    } catch (error) {
                        console.log("error : ");
                        console.log(error);
                    }
                } else {
                    await frappe.call({
                        method: "pp_addon.api.auto_save_doc",
                        args:{
                            obj: this.doc,
                        },
                        callback: (r) => {
                            console.log(r);
                        },
                    });
                }
            });
        }
    }
}


function check_mandatory(frm) {
    var has_errors = false;
    frm.scroll_set = false;

    if (frm.doc.docstatus == 2) return true; // don't check for cancel

    $.each(frappe.model.get_all_docs(frm.doc), function (i, doc) {
        var error_fields = [];
        var folded = false;

        $.each(frappe.meta.docfield_list[doc.doctype] || [], function (i, docfield) {
            if (docfield.fieldname) {
                const df = frappe.meta.get_docfield(doc.doctype, docfield.fieldname, doc.name);

                if (df.fieldtype === "Fold") {
                    folded = frm.layout.folded;
                }

                if (
                    is_docfield_mandatory(doc, df) &&
                    !frappe.model.has_value(doc.doctype, doc.name, df.fieldname)
                ) {
                    has_errors = true;
                    error_fields[error_fields.length] = __(df.label);
                    // scroll to field
                    if (!frm.scroll_set) {
                        let f = doc.parentfield || df.fieldname;
                        scroll_to(frm, f);
                    }

                    if (folded) {
                        frm.layout.unfold();
                        folded = false;
                    }
                }
            }
        });

        if (frm.is_new() && frm.meta.autoname === "Prompt" && !frm.doc.__newname) {
            has_errors = true;
            error_fields = [__("Name"), ...error_fields];
        }

        if (error_fields.length) {
            let meta = frappe.get_meta(doc.doctype);
            let message;
            if (meta.istable) {
                const table_field = frappe.meta.docfield_map[doc.parenttype][doc.parentfield];

                const table_label = __(
                    table_field.label || frappe.unscrub(table_field.fieldname)
                ).bold();

                message = __("Mandatory fields required in table {0}, Row {1}", [
                    table_label,
                    doc.idx,
                ]);
            } else {
                message = __("Mandatory fields required in {0}", [__(doc.doctype)]);
            }
            message = message + "<br><br><ul><li>" + error_fields.join("</li><li>") + "</ul>";
            // frappe.msgprint({
            //     message: message,
            //     indicator: "red",
            //     title: __("Missing Fields"),
            // });
            // frm.refresh();
        }
    });

    return !has_errors;
};

function is_docfield_mandatory(doc, df) {
    if (df.reqd) return true;
    if (!df.mandatory_depends_on || !doc) return;

    let out = null;
    let expression = df.mandatory_depends_on;
    let parent = frappe.get_meta(df.parent);

    if (typeof expression === "boolean") {
        out = expression;
    } else if (typeof expression === "function") {
        out = expression(doc);
    } else if (expression.substr(0, 5) == "eval:") {
        try {
            out = frappe.utils.eval(expression.substr(5), { doc, parent });
            if (parent && parent.istable && expression.includes("is_submittable")) {
                out = true;
            }
        } catch (e) {
            frappe.throw(__('Invalid "mandatory_depends_on" expression'));
        }
    } else {
        var value = doc[expression];
        if ($.isArray(value)) {
            out = !!value.length;
        } else {
            out = !!value;
        }
    }

    return out;
};

function scroll_to(frm, fieldname){
    frm.scroll_to_field(fieldname);
    frm.scroll_set = true;
};

// Function to check if the device is mobile
function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}
