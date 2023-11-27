
// async function sleep(ms) {
//     return await new Promise(resolve => setTimeout(resolve, ms));
// }

// frappe.require(
// 	['assets/pp_addon/node_modules/frappe-gantt/dist/frappe-gantt.js'],
// 	(p) => {
//         var TempGanttView = frappe.views.GanttView;
// 		frappe.views.GanttView = class GanttView extends Gantt {
//             constructor(wrapper, tasks, options) {
//                 console.log(wrapper);
//                 console.log(tasks);
//                 const t = new TempGanttView({
//                     doctype: wrapper.doctype,
//                     parent: wrapper.parent,
//                 });
//                 sleep(100000000)
//                 console.log(t);
//                 wrapper = ".gantt";
//                 tasks = [
//                     {
//                         id: 'Task 1',
//                         name: 'Buy hosting',
//                         start: '2022-01-22',
//                         end: '2022-01-23',
//                         progress: 100,
//                     },
//                     {
//                         id: 'Task 2',
//                         name: 'Draw wireframes',
//                         start: '2022-01-23',
//                         end: '2022-01-25',
//                         progress: 100,
//                     },
//                     {
//                         id: 'Task 3',
//                         name: 'Visual Design',
//                         start: '2022-01-25',
//                         end: '2022-01-27',
//                         progress: 20,
//                         dependencies: 'Task 2'
//                     },
//                     {
//                         id: 'Task 4',
//                         name: 'Build frontend',
//                         start: '2022-02-01',
//                         end: '2022-02-03',
//                         progress: 0,
//                         dependencies: 'Task 3'
//                     },
//                     {
//                         id: 'Task 5',
//                         name: 'Build backend',
//                         start: '2022-02-03',
//                         end: '2022-02-07',
//                         progress: 0,
//                     },
//                     {
//                         id: 'Task 6',
//                         name: 'Deploy Website',
//                         start: '2022-02-07',
//                         end: '2022-02-09',
//                         progress: 0,
//                         dependencies: 'Task 4, Task 5'
//                     },
//                 ]
//                 setTimeout(super(".gantt", tasks), 100000000000000);
//             }
//         }
// 	}
// );