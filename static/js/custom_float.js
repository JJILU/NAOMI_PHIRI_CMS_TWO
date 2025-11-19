$(function() {
  var dataTotal = [[0,200],[1,210],[2,220],[3,230],[4,240]];
  var dataAttendance = [[0,120],[1,125],[2,130],[3,128],[4,135]];
  var dataAssignments = [[0,60],[1,70],[2,65],[3,75],[4,80]];
  var dataPending = [[0,30],[1,25],[2,28],[3,20],[4,18]];

  $.plot("#flot-classroom-chart", [
      { data: dataTotal, label: "Total Students", lines: { show: true, fill: 0.2 } },
      { data: dataAttendance, label: "Attendance Today", lines: { show: true, fill: 0.2 } },
      { data: dataAssignments, label: "Assignments Submitted", lines: { show: true, fill: 0.2 } },
      { data: dataPending, label: "Pending Assignments", lines: { show: true, fill: 0.2 } }
  ], {
      xaxis: {
          ticks: [[0,"Week 1"],[1,"Week 2"],[2,"Week 3"],[3,"Week 4"],[4,"Week 5"]]
      },
      yaxis: { min: 0 },
      grid: { hoverable: true, borderWidth: 1, borderColor: "#ddd" },
      legend: { position: "nw" }
  });
});