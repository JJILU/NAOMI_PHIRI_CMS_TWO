from random import choice

chat_bot_responses = {

    # ========================= BASIC GREETINGS =========================
    "greeting": [
        "👋 Hello! How can I help you today?",
        "😊 Hi there! What would you like to do today?",
        "Welcome back! Ready when you are.",
        "Hey! Need help with attendance, assignments, grades or admin tasks?"
    ],

    # ========================= AUTHENTICATION =========================
    "auth": [
        "To log in, enter your username and password on the login page.",
        "If you're logged out, you'll be redirected back to the login page.",
        "Only authenticated users can access the dashboard and other menus."
    ],

    "logout": [
        "To log out, click the *Logout* link on the menu. You'll be redirected to login.",
        "You have been logged out. See you next time! 👋",
        "Logout successful — come back soon!"
    ],

    # ========================= DASHBOARD =========================
    "dashboard": [
        "Your dashboard shows a quick overview of students, attendance, grades and activities.",
        "From the dashboard, you can navigate to any part of the classroom system.",
        "The dashboard gives school-wide statistics for teachers and admins."
    ],

    # ========================= PROFILE =========================
    "profile": [
        "You can update your personal profile under the **Profile** page.",
        "Profile photos are stored automatically when uploaded.",
        "Teachers and students have separate school records linked to their profiles."
    ],

    # ========================= STUDENT MANAGEMENT =========================
    "student_management": [
        "Manage students under **Students Management → View Students**.",
        "To add new students, open **Students Management → Add Student**.",
        "You can view CMS students under **Students Management → View CMS Students**.",
        "Each student has a linked school record you can update anytime.",
        "Student classroom assignment is handled in the CMS student section."
    ],

    # ========================= TEACHER MANAGEMENT =========================
    "teacher_management": [
        "Teachers can be viewed and managed under the Teacher Management menu.",
        "Teacher records include profile info, school assignment, and role."
    ],

    # ========================= ADMIN MANAGEMENT =========================
    "admin_management": [
        "Admins can be added under **Admin Management → Add Admin**.",
        "To view all admins, open **Admin Management → View Admins**.",
        "Admin accounts are linked to SchoolRecord entries marked as administrators."
    ],

    # ========================= ATTENDANCE =========================
    "attendance_info": [
        "To check attendance, go to **Attendance → View Students Attendance**.",
        "Attendance logs are recorded and displayed in the Attendance dashboard.",
        "Teachers can view daily and monthly attendance reports."
    ],

    "student_attendance": [
        "Students can check attendance under **Student → View Attendances**.",
        "Open the Student panel and click *View Attendances*.",
    ],

    # ========================= CLASSROOMS =========================
    "classroom": [
        "You can manage classrooms under **Classroom → View Classrooms**.",
        "To add a classroom, go to **Classroom → Add Classroom**.",
        "Classrooms are linked to subjects, students, and teachers."
    ],

    # ========================= SUBJECTS =========================
    "subjects": [
        "You can manage subjects under **Subjects → View Subjects**.",
        "To register a subject, go to **Subjects → Add Subject**.",
        "Students and teachers are assigned subjects via classroom CMS records."
    ],

    # ========================= ASSIGNMENTS =========================
    "assignments_teacher": [
        "Teachers can create assignments under **Assignments → Create Assignment**.",
        "You can upload assignment files and instructions under the Assignments menu.",
        "To manage all assignments, open **Assignments → View All Assignments**."
    ],

    "assignments_student": [
        "Students can submit assignments under **Assignment Submission → Submit Assignment**.",
        "To view your submitted assignments, open **Assignment Submission → Submitted Assignments**.",
        "Assignment files uploaded by teachers appear in the Assignments section."
    ],

    # ========================= GRADING =========================
    "grading_teacher": [
        "You can add or update grades under **Grades → Add / View Grades**.",
        "Teachers can generate student performance reports in the Grades section.",
        "To grade assignments, navigate to the Grades menu."
    ],

    "grading_student": [
        "Students can view grades under **Student → View Grades**.",
        "Your academic performance appears in the Student Grades section."
    ],

    # ========================= FILE UPLOADS =========================
    "file_uploads": [
        "Profile photos are stored under the profile_photo uploads folder.",
        "Assignments go into the assignments_uploads folder.",
        "Student submissions are stored separately in *assignment_student_submission_files*."
    ],

    # ========================= TIMETABLE =========================
    "timetable": [
        "You can view the timetable under the Timetable section.",
        "Teachers and students can access scheduled subjects from the timetable page.",
        "Timetables are linked to classrooms and subjects."
    ],

    # ========================= ANNOUNCEMENTS =========================
    "announcements": [
        "Announcements appear on the dashboard once published.",
        "Admins and teachers can post important notices for students.",
        "You can manage announcements under the Announcements section."
    ],

    # ========================= EVENTS =========================
    "events": [
        "School events can be viewed from the Events menu.",
        "Admins can create new events under the Event Management section.",
        "Events help notify students and teachers about important dates."
    ],

    # ========================= SETTINGS =========================
    "settings": [
        "You can update system settings under the Settings menu.",
        "Settings include profile updates, theme options, and preferences.",
        "Only authorized users can modify sensitive settings."
    ],

    # ========================= CMS =========================
    "cms_info": [
        "The CMS manages classrooms, subjects, student assignments, and attendance.",
        "CMS Students section is where you update classroom and subject mappings.",
        "Your Classroom Management System powers all student and teacher data."
    ],

    # ========================= SUPPORT =========================
    "support": [
        "If something isn’t working, contact your system administrator.",
        "For technical support, please notify your teacher or admin.",
        "Need help? I can guide you to the right menu — just ask!"
    ],

    # ========================= ERROR HANDLING =========================
    "error": [
        "Something went wrong. Try again later.",
        "That's not available right now. Please contact the admin.",
        "I couldn't process that — maybe try asking in another way?"
    ],

    # ========================= FALLBACK =========================
    "fallback": [
        "🤔 I’m not sure I understand. Can you ask another way?",
        "I didn't catch that. Try asking about attendance, assignments, grades, admins, or students.",
        "Hmm… I couldn’t match that. What would you like to do?"
    ]
}
