/**
 * Determines whether a given date string represents today's date.
 * @param {String} date A date string, in the format YYYY-MM-DD.
 * @returns True if the given date is today.
 */
function isDateStringToday(date) {
    const today = new Date();
    [year, month, day] = date.split('-').map(x => parseInt(x));
    return today.getFullYear() == year && today.getMonth() + 1 == month && today.getDate() == day;
}

/**
 * Calculates the number of rows required for the HTML calendar.
 * @param {Number} year The year for the calendar.
 * @param {Number} month The month for the calendar, between 1 and 12.
 * @returns {Number} The number of rows required.
 */
function rowsForCalendar(year, month) {
    let currentDate = new Date(year, month - 1, 1);

    // If it's Monday, the first row will be added by the loop
    var result = currentDate.getDay() == 1 ? 0 : 1;

    while (currentDate.getMonth() + 1 == month) {
        if (currentDate.getDay() == 1) {
            result++;
        }

        currentDate.setDate(currentDate.getDate() + 1);
    }

    return result;
}

/**
 * Gets the required height of a given row.
 * @param {Number} index The index of this row, starting from 0, excluding the header.
 * @param {*} rows The total number of rows, excluding the header.
 * @returns {Number} The height of the row in pixels.
 */
function calendarRowHeight(index, rows) {
    // Due to Cursed Stuff, presumably borders, heights differ by a few pixels
    // between different numbers of rows.
    return {
        4: [123, 121, 121, 121],
        5: [98, 97, 97, 97, 97],
        6: [51, 50, 50, 50, 50, 50]
    }[rows][index];
}

/**
 * Reloads the HTML calendar.
 * @param {Number} year The year for the calendar.
 * @param {Number} month The month for the calendar, between 1 and 12.
 */
async function loadCalendar(year, month) {
    closeInfoPanel();
    coverCalendar();

    const calendarElement = document.getElementById('calendar');
    const tableRows = document.querySelectorAll('#calendar tbody tr');
    
    // If this is the first load, predict the number of rows
    if (!calendarElement.dataset.month) {
        const predictedNumberOfRows = rowsForCalendar(year, month);
        for (let i = 0; i < 6; i++) {
            const tableRow = tableRows[i];

            if (i < predictedNumberOfRows) {
                tableRow.classList.remove('hidden');
                
                let thisRowHeight = calendarRowHeight(i, predictedNumberOfRows);
                tableRow.setAttribute("style", `height: ${thisRowHeight}px`);
            } else {
                tableRow.classList.add('hidden');
            }
        }
    }

    // Write data attributes for next/previous month
    calendarElement.dataset.month = month;
    calendarElement.dataset.year = year;

    // Write title
    const months = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    document.getElementById('calendar-current-date').innerHTML = `${months[month]} ${year}`
    
    // Load data from API
    const calendarJson = await fetch(`https://api.hacksoc.org/calendar/events/${year}/${month}/calendar`);
    const calendar = await calendarJson.json();

    // Calculate heights
    const numberOfRows = calendar.filter(x => x).length;

    for (let iRow = 0; iRow < 6; iRow++) {
        const tableRow = tableRows[iRow];
        const dataRow = calendar[iRow];

        // We don't always need all six rows of the calendar to show the entire
        // month's events
        if (dataRow) {
            tableRow.classList.remove('hidden');
        } else {
            tableRow.classList.add('hidden');
            continue;
        }

        // Fixed height is used for each row
        let thisRowHeight = calendarRowHeight(iRow, numberOfRows);
        tableRow.setAttribute("style", `height: ${thisRowHeight}px`);

        for (let iCol = 0; iCol < 7; iCol++) {
            const tableCell = tableRow.children[iCol];
            const dataCell = dataRow[iCol];
    
            // Populate top of cell with date
            tableCell.querySelector('.date-header').innerHTML = dataCell.day;

            // Style the cell
            tableCell.classList.remove('today');
            if (isDateStringToday(dataCell.date)) {
                tableCell.classList.add('today');
            }
            tableCell.classList.remove('disabled');
            if (!dataCell.in_month) {
                tableCell.classList.add('disabled');
            }

            // Reset events text and add each event
            tableCell.querySelector('.events').innerHTML = '';
            dataCell.events.forEach(event => {
                const link = document.createElement("a");
                link.innerHTML = `<b>${event.when_human.start_time}</b> <br class="time-sep" />${event.summary}`;
                link.href = "#";
                link.className = "event-link";
                link.onclick = (e) => {
                    e.preventDefault();
                    displayInfoPanel(link, event);
                    return false;
                };

                tableCell.querySelector('.events').appendChild(link);
                tableCell.querySelector('.events').appendChild(document.createElement('br'));
            }); 
        }
    }

    uncoverCalendar();
};

/**
 * Moves the calendar forwards one month. This requires that the calendar has
 * already been loaded once, so as to set its data-month and data-year
 * attributes.
 */
async function calendarNextMonth() {
    const calendarElement = document.getElementById('calendar');
    let newMonth = parseInt(calendarElement.dataset.month) + 1;
    let newYear = parseInt(calendarElement.dataset.year);
    if (newMonth == 13) {
        newMonth = 1;
        newYear++;
    }

    await loadCalendar(newYear, newMonth);
}

/**
 * Moves the calendar backwards one month. This requires that the calendar has
 * already been loaded once, so as to set its data-month and data-year
 * attributes.
 */
async function calendarPreviousMonth() {
    const calendarElement = document.getElementById('calendar');
    let newMonth = parseInt(calendarElement.dataset.month) - 1;
    let newYear = parseInt(calendarElement.dataset.year);
    if (newMonth == 0) {
        newMonth = 12;
        newYear--;
    }

    await loadCalendar(newYear, newMonth);
}

/**
 * Covers the calendar's table for when it is loading.
 */
function coverCalendar() {
    const tbody = document.querySelector('#calendar tbody');
    const cover = document.getElementById('calendar-loading-cover');
    cover.setAttribute('style', `
        top: ${tbody.offsetTop}px;
        left: ${tbody.offsetLeft}px;
        height: ${tbody.clientHeight}px;
        width: ${tbody.clientWidth}px;
    `);
}

/**
 * Removes the calendar's cover for when it is done loading.
 */
function uncoverCalendar() {
    const cover = document.getElementById('calendar-loading-cover');
    cover.setAttribute('style', 'display: none;');
}

/**
 * Shows the event info panel. The panel is moved in the DOM to the parent of
 * the given target.
 * @param {HTMLElement} target 
 * @param {Object} event 
 */
function displayInfoPanel(target, event) {
    const calendar = document.getElementById('calendar');
    const infoPanelContainer = document.getElementById('calendar-info-container');
    const infoPanel = document.getElementById('calendar-info');
    target.parentElement.appendChild(infoPanelContainer);
    infoPanelContainer.classList.add('showing');

    infoPanel.setAttribute("style", "");

    // Check that the box is inside the calendar horizontally, and translate it
    // if not
    if (infoPanel.getBoundingClientRect().right > calendar.getBoundingClientRect().right) {
        const difference = infoPanel.getBoundingClientRect().right - calendar.getBoundingClientRect().right;
        infoPanel.setAttribute("style", `transform: translateX(-${difference}px);`);
    }

    document.getElementById('calendar-info-title').innerText = event.summary;
    document.getElementById('calendar-info-when').innerText =
        `${event.when_human.start_time}–${event.when_human.end_time} ${event.when_human.long_start_date}`
    document.getElementById('calendar-info-where').innerText = event.location;

    const desc = document.getElementById('calendar-info-description');
    desc.innerHTML = event.description;
    while (desc.firstChild.nodeName.toLowerCase() == "br") {
        desc.removeChild(desc.firstChild);
    }

    // Only show the "Join Meeting" box if there's a meeting to join, and set
    // the correct href
    const meetingButton = document.getElementById('calendar-join-button');
    if (event.meeting_link) {
        meetingButton.href = event.meeting_link;
        meetingButton.classList.remove("hidden");
    } else {
        meetingButton.classList.add("hidden");
    }
}

/**
 * Close the event info panel. The panel stays where it was in DOM.
 */
function closeInfoPanel() {
    const calendar = document.getElementById('calendar');
    const infoPanelContainer = document.getElementById('calendar-info-container');
    infoPanelContainer.classList.remove('showing');
    calendar.appendChild(infoPanelContainer);
}

loadCalendar(new Date().getFullYear(), new Date().getMonth() + 1);
