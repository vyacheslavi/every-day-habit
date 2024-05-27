const date = new Date();

const renderTableHeader = () => {
  date.setDate(1);

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

  const daysArray = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

  const firstDayIndex = date.getDay();

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

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

  document.getElementById("date-string").innerHTML = `${
    months[date.getMonth()]
  }, ${date.getFullYear()}`;
};

function renderTableString(habitName, goal, achieved) {
  date.setDate(1);

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  let habitRow = `<tr class="table-row"><td class="cell-habit-name">${habitName}</td>`;

  for (let i = 1; i <= lastDay; i++) {
    habitRow += `<th class="cell data-index="${i}" data-type="${habitName}"></th>`;
  }

  habitRow += `<td class="cell-goal">${goal}</td>`;
  habitRow += `<td class="cell-achieved">${achieved}</td></tr>`;

  document.getElementById("t-body").insertAdjacentHTML("beforeend", habitRow);
}

renderTableHeader();
renderTableString("lorem", 4, 3);

document.getElementById("left-arrow").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  console.log(date.getMonth());
  renderTableHeader();
  renderTableString("lorem", 4, 3);
});

document.getElementById("rigth-arrow").addEventListener("click", () => {
  date.setMonth(date.getMonth() + 1);
  console.log(date.getMonth());
  renderTableHeader();
  renderTableString("lorem", 4, 3);
});

const endpoint = new URL(`http://127.0.0.1:8000/complete_days/get_days`);

const response = fetch(endpoint);
