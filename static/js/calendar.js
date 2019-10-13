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
 * Reloads the HTML calendar.
 * @param {Number} year The year for the calendar.
 * @param {Number} month The month for the calendar, between 1 and 12.
 */
async function loadCalendar(year, month) {
    closeInfoPanel();
    coverCalendar();

    // Write data attributes for next/previous month
    const calendarElement = document.getElementById('calendar');
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
    // It's too hard to do this mathematically because of border collapsing, so
    // just use a table
    const numberOfRows = calendar.filter(x => x).length;
    const eachRowHeight = {
        4: 121,
        5: 97,
        6: 50
    }[numberOfRows];

    const tableRows = document.querySelectorAll('#calendar tbody tr');
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

        // More cursed height calculation to fix heights being one or two by
        // making the first row slightly taller
        let thisRowHeight = eachRowHeight;
        if (iRow == 0) {
            thisRowHeight++;
            if (numberOfRows == 4) thisRowHeight++;
        }
        tableRow.setAttribute("style", `height: ${thisRowHeight}px`);

        for (let iCol = 0; iCol < 7; iCol++) {
            const tableCell = tableRow.children[iCol];
            const dataCell = dataRow[iCol];
    
            // Populate top of cell with date
            tableCell.querySelector('.date-header').innerHTML = dataCell.day;

            // Style the cell
            tableCell.classList.remove('today');
            tableCell.classList.remove('disabled');
            if (!dataCell.in_month) {
                tableCell.classList.add('disabled');
            } else if (isDateStringToday(dataCell.date)) {
                tableCell.classList.add('today');
            }

            // Reset events text and add each event
            tableCell.querySelector('.events').innerHTML = '';
            dataCell.events.forEach(event => {
                const link = document.createElement("a");
                link.innerHTML = `<b>${event.when_human.start_time}</b> <br class="time-sep" />${event.summary}`;
                link.href = "#";
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
        display: block;
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

    const desc = document.getElementById('calendar-info-description');
    desc.innerHTML = event.description;
    while (desc.firstChild.nodeName.toLowerCase() == "br") {
        desc.removeChild(desc.firstChild);
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
