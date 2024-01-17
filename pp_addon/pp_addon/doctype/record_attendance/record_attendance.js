// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Record Attendance", {
	setup(frm) {
        if (!frm.is_new()) {return;}
        if (frappe.session.user !== "Administrator") {
            frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name", function(r) {
                if (Object.keys(r).length > 0) {
                    frm.set_value("name1", r.name);
                    frm.refresh_field("name");
                }
            });
        }

        // Make Attendance / Leave Time READ ONLY from 08:30:00 AM to 16:00:00 PM
        if (check_time(frm)) {
            frm.set_value("attendance_time", frappe.datetime.now_datetime());
            frm.refresh_field("attendance_time");
        }
        else {
            frm.set_value("attendance_time", frappe.datetime.get_today() + ' 08:00:00');
            frm.refresh_field("attendance_time");
        }
	},

    onload(frm) {
        if (!frm.is_new()) {return;}
        function onPositionRecieved(position) {
            var longitude = position.coords.longitude;
            var latitude = position.coords.latitude;
            frm.set_value('longitude', longitude);
            frm.set_value('latitude', latitude);
            console.log(longitude);
            console.log(latitude);
            // fetch('https://api.opencagedata.com/geocode/v1/json?q='+latitude+'+'+longitude+'&key=de1bf3be66b546b89645e500ec3a3a28')
            fetch('https://api.opencagedata.com/geocode/v1/json?key=9b5da18b49974108b8064bed3c84e7e3&q=' + latitude + '+' + longitude + '')
                .then(response => response.json())
                .catch(err => console.log(err));
            frm.set_df_property('location', 'options', '<div class="mapouter"><div class="gmap_canvas"><iframe width=100% height="300" id="gmap_canvas" src="https://maps.google.com/maps?q=' + latitude + ',' + longitude + '&t=&z=17&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://yt2.org/youtube-to-mp3-ALeKk00qEW0sxByTDSpzaRvl8WxdMAeMytQ1611842368056QMMlSYKLwAsWUsAfLipqwCA2ahUKEwiikKDe5L7uAhVFCuwKHUuFBoYQ8tMDegUAQCSAQCYAQCqAQdnd3Mtd2l6"></a><br><style>.mapouter{position:relative;text-align:right;height:300px;width:100%;}</style><style>.gmap_canvas {overflow:hidden;background:none!important;height:300px;width:100%;}</style></div></div>');
            frm.refresh_field('location');
        }

        function locationNotRecieved(positionError) {
            frm.set_df_property("location_section", "hidden", 1);
            console.log(positionError);
        }

        if (frm.doc.longitude && frm.doc.latitude) {
            frm.set_df_property('location', 'options', '<div class="mapouter"><div class="gmap_canvas"><iframe width=100% height="300" id="gmap_canvas" src="https://maps.google.com/maps?q=' + frm.doc.latitude + ',' + frm.doc.longitude + '&t=&z=17&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://yt2.org/youtube-to-mp3-ALeKk00qEW0sxByTDSpzaRvl8WxdMAeMytQ1611842368056QMMlSYKLwAsWUsAfLipqwCA2ahUKEwiikKDe5L7uAhVFCuwKHUuFBoYQ8tMDegUAQCSAQCYAQCqAQdnd3Mtd2l6"></a><br><style>.mapouter{position:relative;text-align:right;height:300px;width:100%;}</style><style>.gmap_canvas {overflow:hidden;background:none!important;height:300px;width:100%;}</style></div></div>');
            frm.refresh_field('location');
        } else {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(onPositionRecieved, locationNotRecieved, { enableHighAccuracy: true });
            }
        }
    },

    log_type(frm) {
        if (frm.doc.log_type === "IN") {
            if (check_time(frm)) {
                frm.set_value("attendance_time", frappe.datetime.now_datetime());
                frm.refresh_field("attendance_time");
            }
            else {
                frm.set_value("attendance_time", frappe.datetime.get_today() + ' 08:00:00');
                frm.refresh_field("attendance_time");
            }
        }
        else if (frm.doc.log_type === "OUT") {
            if (check_time(frm)) {
                frm.set_value("attendance_time", frappe.datetime.now_datetime());
                frm.refresh_field("attendance_time");
            }
            else {
                frm.set_value("attendance_time", frappe.datetime.get_today() + ' 16:00:00');
                frm.refresh_field("attendance_time");
            }
        }
        else if (in_list(["Exit", "Enter"], frm.doc.log_type)) {
            frm.set_df_property("attendance_time", "read_only", 0);
            frm.set_value("attendance_time", frappe.datetime.now_datetime());
            frm.refresh_field("attendance_time");
        }
    },
});


function check_time(frm) {
    // Make Attendance / Leave Time READ ONLY from 08:30:00 AM to 16:00:00 PM
    const EIGHT_OBJ = new Date().setHours(8, 30, 0);
    const FOUR_OBJ = new Date().setHours(16, 0, 0);
    const NOW_OBJ = frappe.datetime.now_time(true);
    if (NOW_OBJ.getTime() >= EIGHT_OBJ && NOW_OBJ.getTime() <= FOUR_OBJ) {
        frm.set_df_property("attendance_time", "read_only", 1);
        return true;
    }
    else {
        frm.set_df_property("attendance_time", "read_only", 0);
        return false;
    }
}
