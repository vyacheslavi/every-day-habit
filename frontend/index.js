const date = new Date();

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const daysArray = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];

const firstDayIndex = date.getDay();

const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

function renderTable() {
  const monthDays = document.querySelector(".month-days");
  const monthWeekDays = document.querySelector(".days-of-week");

  let daysNumbers = "";
  let weekDays = `<th rowspan="2" class="align-middle">Habit</th>`;
  let dayIndex = firstDayIndex;

  for (let i = 1; i <= lastDay; i++) {
    daysNumbers += `<th class="day">${i}</th>`;
    if (dayIndex > 6) {
      dayIndex = 0;
    }
    weekDays += `<th>${daysArray[dayIndex]}</th>`;
    dayIndex += 1;
  }
  weekDays += `<th rowspan="2" class="align-middle">Goal</th><th rowspan="2" class="align-middle">Achieved</th>`;
  monthWeekDays.innerHTML = weekDays;
  monthDays.innerHTML = daysNumbers;
  document.getElementById("date-string").innerHTML = months[date.getMonth()];
}

function renderTableString(habitName, goal, achieved) {
  let habitRow = `<td class="cell-habit-name">${habitName}</td>`;

  for (let i = 1; i <= lastDay; i++) {
    habitRow += `<th class="cell data-index="${i}" data-type="${habitName}"></th>`;
  }

  document.getElementById("date-string").innerHTML = `${
    months[date.getMonth()]
  }, ${date.getFullYear()}`;
}
// document
//   .querySelector(".bi bi-caret-left-fill")
//   .addEventListener("click", () => {
//     date.setMonth(date.getMonth() - 1);
//     renderCalendar();
//   });

// document.querySelector(".next").addEventListener("click", () => {
//   date.setMonth(date.getMonth() + 1);
//   renderCalendar();
// });

// document.querySelector(".days-of-week").innerHTML = ;

renderTable();
