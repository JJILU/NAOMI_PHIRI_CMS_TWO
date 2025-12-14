// document.addEventListener("DOMContentLoaded", function () {

// $(function() {
//     // Read chart data from HTML
//     var totalData = JSON.parse($('#flot-classroom-chart').data('total'));
//     var attendanceData = JSON.parse($('#flot-classroom-chart').data('attendance'));
//     var assignmentsData = JSON.parse($('#flot-classroom-chart').data('assignments'));
//     var pendingData = JSON.parse($('#flot-classroom-chart').data('pending'));

//     $.plot("#flot-classroom-chart", [
//         { data: totalData, label: "Total Students", lines: { show: true, fill: 0.2 } },
//         { data: attendanceData, label: "Attendance Today", lines: { show: true, fill: 0.2 } },
//         { data: assignmentsData, label: "Assignments Submitted", lines: { show: true, fill: 0.2 } },
//         { data: pendingData, label: "Pending Assignments", lines: { show: true, fill: 0.2 } }
//     ], {
//         xaxis: { ticks: [[0,"Mon"],[1,"Tue"],[2,"Wed"],[3,"Thu"],[4,"Fri"],[5,"Sat"],[6,"Sun"]] },
//         yaxis: { min: 0 },
//         grid: { hoverable: true, borderWidth: 1, borderColor: "#ddd" },
//         legend: { position: "nw" }
//     });
// });

// })
