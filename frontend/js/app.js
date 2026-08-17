const video =
    document.getElementById("video");

const statusText =
    document.getElementById("status");

const recognitionStatus =
    document.getElementById("recognitionStatus");

const employeeId =
    document.getElementById("employeeId");

const employeeName =
    document.getElementById("employeeName");

const similarity =
    document.getElementById("similarity");

const attendance =
    document.getElementById("attendance");

const cameraIndicator =
    document.getElementById("cameraIndicator");

const attendanceContainer =
    document.getElementById(
        "attendanceTableContainer"
    );


let stream = null;

let recognitionInterval = null;

let isProcessing = false;

let lastRecognizedEmployee = null;


const canvas =
    document.createElement("canvas");


/* =========================================
   START CAMERA
========================================= */

document
    .getElementById("startBtn")
    .onclick = async () => {

        try {

            stream =
                await navigator.mediaDevices
                    .getUserMedia({
                        video: true,
                        audio: false
                    });


            video.srcObject = stream;


            statusText.innerText =
                "Camera active - scanning...";

            statusText.className =
                "status info";


            cameraIndicator.innerText =
                "● Online";

            cameraIndicator.className =
                "indicator online";


            recognitionStatus.innerText =
                "Looking for employee...";

            recognitionStatus.className =
                "status info";


            /*
             * Capture a frame every 2 seconds.
             */

            recognitionInterval =
                setInterval(
                    sendFrame,
                    2000
                );


        } catch (error) {

            console.error(error);


            statusText.innerText =
                "Unable to access camera.";

            statusText.className =
                "status warning";


            cameraIndicator.innerText =
                "● Offline";

            cameraIndicator.className =
                "indicator offline";
        }
    };


/* =========================================
   SEND CAMERA FRAME
========================================= */

async function sendFrame() {

    if (isProcessing) {
        return;
    }


    if (
        !video.videoWidth ||
        !video.videoHeight
    ) {
        return;
    }


    isProcessing = true;


    canvas.width =
        video.videoWidth;

    canvas.height =
        video.videoHeight;


    const context =
        canvas.getContext("2d");


    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );


    canvas.toBlob(
        async (blob) => {

            if (!blob) {

                isProcessing = false;

                return;
            }


            const formData =
                new FormData();


            formData.append(
                "file",
                blob,
                "camera_frame.jpg"
            );


            try {

                const response =
                    await fetch(
                        "/recognition/camera",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                if (!response.ok) {
                    throw new Error(
                        "Recognition request failed"
                    );
                }


                const data =
                    await response.json();


                console.log(
                    "Recognition:",
                    data
                );


                /* =========================
                   RECOGNIZED
                ========================= */

                if (data.recognized) {

                    updateRecognitionResult(
                        data
                    );


                    /*
                     * Load attendance only when
                     * a new employee is recognized.
                     */

                    if (
                        lastRecognizedEmployee
                        !== data.employee_id
                    ) {

                        lastRecognizedEmployee =
                            data.employee_id;

                        loadTodayAttendance(
                            data.employee_id
                        );
                    }
                }


                /* =========================
                   NOT RECOGNIZED
                ========================= */

                /* =========================
   NOT RECOGNIZED
========================= */

else {

    // Clear previous employee information
    employeeId.innerText = "--";
    employeeName.innerText = "--";
    similarity.innerText = "--";
    attendance.innerText = "--";

    // Reset recognized employee
    lastRecognizedEmployee = null;

    // Update recognition status
    recognitionStatus.innerText =
        "No recognized employee";

    recognitionStatus.className =
        "status warning";

    // Update camera status
    statusText.innerText =
        "Looking for employee...";

    statusText.className =
        "status info";

    // Clear attendance table
    attendanceContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">
                📋
            </div>

            <p>
                No attendance records to display.
            </p>
        </div>
    `;
}

            } catch (error) {

                console.error(
                    "Recognition error:",
                    error
                );


                statusText.innerText =
                    "Recognition service unavailable.";

                statusText.className =
                    "status warning";
            }


            isProcessing = false;

        },
        "image/jpeg"
    );
}


/* =========================================
   UPDATE RECOGNITION RESULT
========================================= */

function updateRecognitionResult(data) {

    employeeId.innerText =
        data.employee_id ?? "--";


    employeeName.innerText =
        data.employee_name ?? "Employee";


    similarity.innerText =
        data.similarity
            ? (
                data.similarity * 100
            ).toFixed(2) + "%"
            : "--";


    attendance.innerText =
        data.attendance ?? "--";


    if (
        data.attendance ===
        "Attendance marked"
    ) {

        recognitionStatus.innerText =
            "✓ Employee Recognized & Attendance Marked";

    } else {

        recognitionStatus.innerText =
            "✓ Employee Recognized";
    }


    recognitionStatus.className =
        "status success";


    statusText.innerText =
        "Employee recognized successfully";

    statusText.className =
        "status success";
}


/* =========================================
   LOAD TODAY'S ATTENDANCE
========================================= */

async function loadTodayAttendance(
    employeeId
) {

    try {

        const today =
            new Date();


        const year =
            today.getFullYear();


        const month =
            String(
                today.getMonth() + 1
            ).padStart(2, "0");


        const day =
            String(
                today.getDate()
            ).padStart(2, "0");


        const todayString =
            `${year}-${month}-${day}`;


        const response =
            await fetch(
                `/attendance/date/${todayString}`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load attendance"
            );
        }


        const records =
            await response.json();


        /*
         * Only show the recognized employee.
         */

        const employeeRecords =
            records.filter(
                record =>
                    Number(record.employee_id)
                    === Number(employeeId)
            );


        if (
            employeeRecords.length === 0
        ) {

            attendanceContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">
                        📋
                    </div>

                    <p>
                        No attendance marked today.
                    </p>
                </div>
            `;

            return;
        }


        attendanceContainer.innerHTML = `

            <table class="attendance-table">

                <thead>

                    <tr>

                        <th>Date</th>

                        <th>Time</th>

                        <th>Status</th>

                    </tr>

                </thead>


                <tbody>

                    ${employeeRecords
                        .map(
                            record => `

                            <tr>

                                <td>
                                    ${record.attendance_date}
                                </td>

                                <td>
                                    ${record.attendance_time}
                                </td>

                                <td class="present">
                                    ✓ Present
                                </td>

                            </tr>
                        `
                        )
                        .join("")
                    }

                </tbody>

            </table>
        `;


    } catch (error) {

        console.error(
            "Attendance history error:",
            error
        );


        attendanceContainer.innerHTML = `

            <div class="empty-state">

                <p>
                    Unable to load attendance.
                </p>

            </div>
        `;
    }
}


/* =========================================
   STOP CAMERA
========================================= */

document
    .getElementById("stopBtn")
    .onclick = () => {


        if (recognitionInterval) {

            clearInterval(
                recognitionInterval
            );

            recognitionInterval =
                null;
        }


        if (stream) {

            stream
                .getTracks()
                .forEach(
                    track =>
                        track.stop()
                );

            stream = null;
        }


        video.srcObject = null;


        statusText.innerText =
            "Camera stopped";

        statusText.className =
            "status info";


        cameraIndicator.innerText =
            "● Offline";

        cameraIndicator.className =
            "indicator offline";


        recognitionStatus.innerText =
            "Waiting for employee...";

        recognitionStatus.className =
            "status info";


        lastRecognizedEmployee =
            null;
    };