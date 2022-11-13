
let baseURL = "http://localhost:5000";
let async = true;
let method;

const tableHeadings = {
    enrolledTableHeadings: ["Name", "Instructor", "Time", "Enrollment"],
    addTableHeadings: ["Add or Remove", "Name", "Instructor", "Time", "Enrollment"],
    instructorCoursesHeadings: ["Name", "Instructor", "Time", "Enrollment"],
    courseGradebookHeadings: ["Student", "Grade"]
}

function updateCourseEnrollmentStatus(studentName, enrollOption, courseName) {
    let xhttp3 = new XMLHttpRequest();

    method = "POST";
    let url = `${baseURL}/home/student/${studentName}`;
    console.log("we here")

    xhttp3.open(method, url, true);
    xhttp3.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp3.send(`course_name=${courseName}&enroll_option=${enrollOption}`);
    console.log("we here2")
}

function generateHTML(tableData, headings, studentName) {
    let headingsHTML = "";
    let tableBodyHTML = "";
    let tableRowLength;
    console.log("we here3")
    for (let i = 0; i < headings.length; i++) {
        headingsHTML += "<th>" + headings[i] + "</th>";
    }

    for (let j = 0; j < tableData.length; j++) {
        tableBodyHTML += "<tr>"

        tableRowLength = Object.keys(tableData[j]).length;

        let startingPosition = 0;

        if (headings === tableHeadings.addTableHeadings) {
            ++startingPosition;

            let enrollOption = tableData[j].enrolled ? "Remove" : "Add";
            let courseName = tableData[j].name;

            tableBodyHTML += 
                `<td>
                    <button class="options-button" onclick="updateCourseEnrollmentStatus('${studentName}', '${enrollOption.toLowerCase()}', '${courseName}')">
                        ${enrollOption}
                    </button>
                </td>`;

        }

        for (let k = startingPosition; k < tableRowLength; k++) {

            tableBodyHTML += '<td>' + tableData[j][headings[k].toLowerCase()] + '</td>';
        }

        tableBodyHTML += "</tr>";

    }

    return {
        headingsHTML,
        tableBodyHTML
    };
}

function generateTable(headingType, dataFromServer, studentName) {
    let headingsRow = document.querySelector(".headings-row");
    let tableBody = document.querySelector(".data-table-body");

    let tableData = dataFromServer;
    console.log("we here6");
    switch (headingType) {
        case ("enrolled"):
            tableHTML = generateHTML(tableData, tableHeadings.enrolledTableHeadings, studentName);console.log("we here10");
            break;
        case ("add"):
            tableHTML = generateHTML(tableData, tableHeadings.addTableHeadings, studentName);console.log("we here9");
            break;
            
    }
    console.log("we here7")
    headingsRow.innerHTML = tableHTML.headingsHTML;
    tableBody.innerHTML = tableHTML.tableBodyHTML;
}


function getTable(nameOfTab, studentName) {
    let enrolledTab = document.querySelector(".enrolled-tab");
    let addTab = document.querySelector(".add-tab");

    // get enrolled table 
    if (nameOfTab === "enrolled") {
        // change tab styling
        if (!enrolledTab.classList.contains("active-tab")) {
            enrolledTab.classList.add("active-tab");
        }
        
        if (addTab.classList.contains("active-tab")) {
            addTab.classList.remove("active-tab");
        }

        let xhttp = new XMLHttpRequest();
        method = "GET";
        let url = `${baseURL}/enrolled/${studentName}`;
        xhttp.open(method, url, async);

        xhttp.onload = function() {
            let enrolledData = JSON.parse(this.response);
            generateTable(nameOfTab, enrolledData, studentName);
        };
        
        xhttp.send();
    }

    // get add table
    else if (nameOfTab === "add") {
        // change tab styling
        if (!addTab.classList.contains("active-tab")) {
            addTab.classList.add("active-tab");
        }

        if (enrolledTab.classList.contains("active-tab")) {
            enrolledTab.classList.remove("active-tab");
        }

        let coursesData;
        let enrolledData;

        let xhttp1 = new XMLHttpRequest();
        let xhttp2 = new XMLHttpRequest();

        method = "GET";
        
        let url1 = `${baseURL}/enrolled/${studentName}`;
        let url2 = `${baseURL}/courses`;

        xhttp1.open(method, url1, async);

        let enrolledCourses = [];

        xhttp1.onload = function() {
            enrolledData = JSON.parse(this.response);

            for (let i = 0; i < enrolledData.length; i++) {
                enrolledCourses.push(enrolledData[i].name);
            }

            xhttp2.open(method, url2, async);

            xhttp2.onload = function() {
                coursesData = JSON.parse(this.response);
                
                let isEnrolled = false;
                for (let i = 0; i < coursesData.length; i++) {
                    for (let j = 0; j < enrolledCourses.length; j++) {
                        if (coursesData[i].name === enrolledCourses[j]) {
                            coursesData[i].enrolled = !isEnrolled;
                            break;
                        }
                        else {
                            coursesData[i].enrolled = isEnrolled;
                        }

                        
                    }
                }

                generateTable(nameOfTab, coursesData, studentName);
            }

            xhttp2.send();
        };

        xhttp1.send();

        // xhttp2.open(method, url2, async);

        // xhttp2.onload = function() {
        //     coursesData = JSON.parse(this.response);
            
        //     console.log(coursesData);

        //     let isEnrolled = false;
        //     for (let i = 0; i < coursesData.length; i++) {
        //         for (let j = 0; j < enrolledCourses.length; j++) {
        //             if (coursesData[i].name === enrolledCourses[j]) {
        //                 coursesData[i].enrolled = !isEnrolled;
        //                 break;
        //             }
        //             else {
        //                 coursesData[i].enrolled = isEnrolled;
        //             }

                    
        //         }
        //     }

        //     generateTable(nameOfTab, coursesData, studentName);
        // }

        // xhttp2.send();
    }
}

function goBack() {
    window.history.back();
  }