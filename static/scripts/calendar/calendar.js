const date = new Date();

// ================================================================================================================================

// Table render functions

// ================================================================================================================================
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

const renderTableHeader = () => {
  date.setDate(1);

  document.getElementById("date-string").innerHTML = `${
    months[date.getMonth()]
  }, ${date.getFullYear()}`;

  const daysArray = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

  const firstDayIndex = date.getDay();

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  const container = document.querySelector(".table-responsive-xl");
  container.replaceChildren();

  const t = document.createElement("table");
  t.classList.add(
    "table",
    "table-bordered",
    "border-light",
    "table-hover",
    "text-center",
    "table-row-fix"
  );
  t.id = "calendar-table";
  container.appendChild(t);

  const thead = document.createElement("thead");
  thead.classList.add("text-center");
  t.appendChild(thead);

  const monthWeekDaysRow = document.createElement("tr");
  monthWeekDaysRow.classList.add("days-of-week");

  const monthDaysRow = document.createElement("tr");
  monthDaysRow.classList.add("month-days");

  thead.appendChild(monthWeekDaysRow);
  thead.appendChild(monthDaysRow);

  var thHabit = document.createElement("th");
  thHabit.rowSpan = "2";
  thHabit.textContent = "Habit";
  thHabit.classList.add("align-middle", "habit-column");
  monthWeekDaysRow.appendChild(thHabit);

  let dayIndex = firstDayIndex;

  for (let i = 1; i <= lastDay; i++) {
    var thDay = document.createElement("th");
    thDay.classList.add("column-day");
    thDay.textContent = i;
    monthDaysRow.appendChild(thDay);
    if (dayIndex > 6) {
      dayIndex = 0;
    }
    var thWeekDay = document.createElement("th");
    thWeekDay.textContent = daysArray[dayIndex];
    monthWeekDaysRow.appendChild(thWeekDay);
    dayIndex += 1;
  }
  var thGoal = document.createElement("th");
  thGoal.rowSpan = "2";
  thGoal.textContent = "Goal";
  thGoal.classList.add("align-middle", "goal-column");
  monthWeekDaysRow.appendChild(thGoal);

  var thAchieved = document.createElement("th");
  thAchieved.rowSpan = "2";
  thAchieved.textContent = "Acheived";
  thAchieved.classList.add("align-middle", "achieved-column");
  monthWeekDaysRow.appendChild(thAchieved);

  var tbody = document.createElement("tbody");
  tbody.classList.add("table-group-divider");
  tbody.id = "t-body";
  t.appendChild(tbody);
};

function renderTableString(habitId, habitName, goal, achieved) {
  date.setDate(1);

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  const tbody = document.getElementById("t-body");

  let habitRow = document.createElement("tr");
  habitRow.classList.add("table-row");

  tbody.appendChild(habitRow);

  // habit cell generation start----------------------------------------------------------------------------------------------------

  var habitHameCell = document.createElement("td");
  var habitHameCellInnerDiv = document.createElement("div");
  habitHameCell.appendChild(habitHameCellInnerDiv);
  habitHameCell.setAttribute("onmouseover", "swapDivsHabitNameCell(this)");
  habitHameCell.setAttribute("onmouseout", "swapDivsHabitNameCell(this)");

  var habitNameSpan = document.createElement("span");
  habitNameSpan.classList.add("habit-name-span");
  habitNameSpan.setAttribute("id", habitId);
  habitNameSpan.textContent = habitName;

  var habitNameTools = document.createElement("div");
  habitNameTools.classList.add("habit-tools");
  habitNameTools.classList.add("d-none");
  habitNameTools.innerHTML = `
  <button type="button" data-bs-toggle="modal" class="btn btn-my" data-bs-target="#delete-habit-modal" data-habit-id=${habitId} data-habit-name=${habitName} data-habit-goal=${goal}>
    <img src="${window.location.origin}/static/img/trash-fill.svg">
  </button>
  <button type="button" data-bs-toggle="modal" class="btn btn-my" data-bs-target="#edit-habit-modal" data-habit-id=${habitId} data-habit-name=${habitName} data-habit-goal=${goal}>
    <img src="${window.location.origin}/static/img/pencil-square.svg">
  </button>
    `;

  habitHameCellInnerDiv.appendChild(habitNameSpan);
  habitHameCellInnerDiv.appendChild(habitNameTools);

  habitRow.appendChild(habitHameCell);

  // habit cell generation end-------------------------------------------------------------------------------------------

  for (let i = 1; i <= lastDay; i++) {
    var habitDayCell = document.createElement("td");
    habitDayCell.classList.add("cell");

    var fullDate = new Date(date.getFullYear(), date.getMonth(), i + 1)
      .toISOString()
      .split("T")[0];
    habitDayCell.setAttribute("data-day", fullDate);
    habitDayCell.setAttribute("data-habitid", habitId);

    habitRow.appendChild(habitDayCell);
  }
  var goalCell = document.createElement("td");
  goalCell.classList.add("cell-goal");
  goalCell.textContent = goal;
  habitRow.appendChild(goalCell);

  var achievedCell = document.createElement("td");
  achievedCell.classList.add("cell-achieved");
  achievedCell.id = `achieved-count-${habitId}`;
  achievedCell.textContent = achieved;
  habitRow.appendChild(achievedCell);
}

async function sendRequestGetCompleteDays(habit_id, year, month) {
  response = await fetch(
    window.location.origin +
      `/api/v1/complete-days/month/${month}/year/${year}/habit-id/${habit_id}`,
    {
      method: "GET",
    }
  );
  if (response.ok) {
    var data = await response.json();
    return data;
  }
  return;
}

async function gethabitList(month, year) {
  const response = await fetch(
    window.location.origin + `/api/v1/habits/month/${month}/year/${year}`,
    {
      method: "GET",
    }
  );
  if (response.ok) {
    var data = await response.json();
    return data;
  }
  return;
}

async function renderHabitRows() {
  const month = date.getMonth() + 1;
  const year = date.getFullYear();
  const habitList = await gethabitList(month, year);

  if (habitList) {
    for (let habit of habitList) {
      renderTableString(habit.id, habit.name, habit.goal, 42);
      const habitId = habit.id;
      daysInRow = await sendRequestGetCompleteDays(habitId, year, month);
      if (daysInRow) {
        var achievedCount = document.getElementById(
          `achieved-count-${habitId}`
        );
        achievedCount.textContent = Object.keys(daysInRow).length;

        for (let day of daysInRow) {
          var dayDate = day.date;

          const element = document.querySelector(
            `[data-day="${dayDate}"][data-habitid="${habitId}"]`
          );
          if (element) {
            element.classList.add("bg-success");

            var checkImg = new Image();
            checkImg.setAttribute(
              "src",
              window.location.origin + "/static/img/check-lg.svg"
            );

            element.appendChild(checkImg);
          }
        }
      }
    }
  }
}
// ================================================================================================================================

// Rendering notes

// ================================================================================================================================

async function sendRequestGetNotes(month, year) {
  response = await fetch(
    window.location.origin + `/api/v1/notes/month/${month}/year/${year}/`,
    {
      method: "GET",
    }
  );
  if (response.ok) {
    var data = await response.json();
    return data;
  }
  return;
}

async function renderNote(parent, noteId, text, createdAt) {
  var firstDiv = document.createElement("div");
  var classesToAdd = ["card", "mb-3"];
  firstDiv.classList.add(...classesToAdd);
  firstDiv.setAttribute("onmouseover", "swapDivsNotesCards(this)");
  firstDiv.setAttribute("onmouseout", "swapDivsNotesCards(this)");

  parent.appendChild(firstDiv);

  var secondDiv = document.createElement("div");
  classesToAdd = ["card-header", "d-flex", "justify-content-between"];
  secondDiv.setAttribute("style", "height: 40px;");
  secondDiv.classList.add(...classesToAdd);
  firstDiv.appendChild(secondDiv);

  var spanDate = document.createElement("span");
  spanDate.textContent = `${createdAt.split("-")[2]} ${
    months[createdAt.split("-")[1] - 1]
  }`;
  spanDate.setAttribute("data-created-at", createdAt);
  secondDiv.appendChild(spanDate);

  var spanTools = document.createElement("span");
  spanTools.id = "note-tools";
  spanTools.classList.add("d-none");

  spanTools.innerHTML = `
    <button type="button" class="btn btn-my" data-bs-toggle="modal" data-bs-target="#edit-note-modal" data-note-id=${noteId}>
      <img src="${window.location.origin}/static/img/pencil-square.svg">
    </button>
    <button type="button ms-3" class=" btn btn-my" data-bs-toggle="modal" data-bs-target="#delete-note-modal" data-note-id=${noteId}>
      <img src="${window.location.origin}/static/img/trash-fill.svg">
    </button>
  `;

  secondDiv.appendChild(spanTools);

  var cardBodyDiv = document.createElement("div");
  cardBodyDiv.classList.add("card-body");
  firstDiv.appendChild(cardBodyDiv);

  var spanText = document.createElement("span");
  classesToAdd = ["text-body-secondary", "card-text"];
  spanText.classList.add(...classesToAdd);
  spanText.textContent = text;
  cardBodyDiv.appendChild(spanText);
}

async function renderNoteDiv() {
  date.setDate(1);

  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  const noteDiv = document.getElementById("note-div");
  const notesHintP = document.getElementById("notes-hint");
  noteDiv.innerHTML = "";
  const notes = await sendRequestGetNotes(month, year);
  if (notes.length !== 0) {
    notesHintP.classList.add("d-none");
    for (let note of notes) {
      await renderNote(noteDiv, note.id, note.text, note.created_at);
    }
  } else {
    notesHintP.classList.remove("d-none");
  }
}

// ================================================================================================================================

// Invoke render functions

// ================================================================================================================================

async function renderTable() {
  renderTableHeader();
  await renderHabitRows();
  await addCellsInteraction();
}

async function renderPage() {
  await renderTable();
  await renderNoteDiv();
}

renderPage();

// ================================================================================================================================

// Swap functions

// ================================================================================================================================

function swapDivsHabitNameCell(element) {
  var nameSpan = element.getElementsByClassName("habit-name-span")[0];
  var toolsDiv = element.getElementsByClassName("habit-tools")[0];

  if (nameSpan.classList.contains("d-none")) {
    nameSpan.classList.remove("d-none");
    toolsDiv.classList.add("d-none");
  } else {
    toolsDiv.classList.remove("d-none");
    nameSpan.classList.add("d-none");
  }
}

function swapDivsNotesCards(element) {
  var toolsElement = element.querySelector("#note-tools");
  if (toolsElement.classList.contains("d-none")) {
    toolsElement.classList.remove("d-none");
  } else {
    toolsElement.classList.add("d-none");
  }
}

// ================================================================================================================================

// Arrows eventlistners

// ================================================================================================================================

document.getElementById("left-arrow").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  renderPage();
});

document.getElementById("right-arrow").addEventListener("click", () => {
  date.setMonth(date.getMonth() + 1);
  renderPage();
});

// ================================================================================================================================

// Cells eventlistners

// ================================================================================================================================

async function addCellsInteraction() {
  const cells = document.querySelectorAll(".cell");
  cells.forEach(function (elem) {
    elem.addEventListener("click", cellsIOfunc);
  });
}

async function cellsIOfunc() {
  if (this.firstChild) {
    this.replaceChildren();
    this.classList = "cell";
    await deleteDay(this.dataset.habitid, this.dataset.day);
  } else {
    completeDay(this.dataset.habitid, this.dataset.day);
    var checkImg = new Image();
    checkImg.setAttribute(
      "src",
      window.location.origin + "/static/img/check-lg.svg"
    );
    this.classList.add("bg-success");
    this.appendChild(checkImg);
  }
}

async function deleteDay(habit_id, day) {
  await fetch(
    window.location.origin +
      `/api/v1/complete-days/?habit_id=${habit_id}&date=${day}`,
    {
      method: "DELETE",
      headers: {
        accept: "application/json",
      },
    }
  );
}

async function completeDay(habitid, day) {
  var cd = {
    habit_id: habitid,
    date: day,
  };

  await fetch(window.location.origin + "/api/v1/complete-days/", {
    method: "POST",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cd),
  });
}

// ================================================================================================================================

// create habit form

// ================================================================================================================================

function formDataToJSON(form) {
  const data = new FormData(form);
  const formDataObject = Object.fromEntries(data);
  return formDataObject;
}

async function sendRequestCreateHabit(data) {
  return await fetch(window.location.origin + "/api/v1/habits/", {
    method: "POST",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
    body: data,
  });
}

async function createHabitFormSubmit(event) {
  // date.setDate(1);
  event.preventDefault();
  button = document.getElementById("create-habit-btn");
  const data = formDataToJSON(createHabitForm);

  var fullDate = new Date(date.getFullYear(), date.getMonth() + 1)
    .toISOString()
    .split("T")[0];

  data["created_at"] = fullDate;

  const response = await sendRequestCreateHabit(JSON.stringify(data));
  if (response.ok) {
    clearFormInModal(createHabitModalWindow._element);
    createHabitModalWindow.hide();
    await renderTable();
    alert("The habit has been created");
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck-create-habit").innerHTML =
        err["detail"];
    });
  }
}

const createHabitForm = document.getElementById("create-habit-form");
createHabitForm.addEventListener("submit", createHabitFormSubmit);

const createHabitModalWindow = new bootstrap.Modal(
  document.getElementById("create-habit-modal")
);

// ================================================================================================================================

// edit habit form

// ================================================================================================================================

async function sendRequestPatchHabit(data, habit_id) {
  return await fetch(window.location.origin + `/api/v1/habits/${habit_id}`, {
    method: "PATCH",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
    body: data,
  });
}

async function editHabitFormSubmit(event) {
  event.preventDefault();
  console.log("habit-wotking");
  const spinner = document.getElementById("spnr");
  spinner.classList.remove("visually-hidden");
  const button = document.getElementById("edit-habit-btn");
  button.disabled = true;

  var habitId = button.getAttribute("data-habit-id");
  const data = formDataToJSON(editHabitForm);

  const response = await sendRequestPatchHabit(JSON.stringify(data), habitId);
  if (response.ok) {
    window.location.reload();
    editHabitModalWindow.hide();
    await renderTable();
    alert("The habit has been edited");
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck-create-habit").innerHTML =
        err["detail"];
    });
  }
  spinner.classList.add("visually-hidden");
  button.disabled = false;
}

const editHabitForm = document.getElementById("edit-habit-form");
editHabitForm.addEventListener("submit", editHabitFormSubmit);

const editHabitModalWindow = new bootstrap.Modal(
  document.getElementById("edit-habit-modal")
);
if (editHabitModalWindow) {
  editHabitModalWindow._element.addEventListener("show.bs.modal", (event) => {
    const button = event.relatedTarget;

    var habitName = button.getAttribute("data-habit-name");
    var habitGoal = button.getAttribute("data-habit-goal");
    var habitId = button.getAttribute("data-habit-id");

    const habitNameInput =
      editHabitModalWindow._element.querySelector("#habit-name");
    const habitGoalInput =
      editHabitModalWindow._element.querySelector("#habit-goal");
    const submitBtn =
      editHabitModalWindow._element.querySelector("#edit-habit-btn");

    habitNameInput.value = habitName;
    habitGoalInput.value = habitGoal;
    submitBtn.setAttribute("data-habit-id", habitId);
  });
}

// ================================================================================================================================

// delete habit modal

// ================================================================================================================================

async function sendRequestDeleteHabit(habit_id) {
  return await fetch(window.location.origin + `/api/v1/habits/${habit_id}`, {
    method: "DELETE",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
  });
}

const deleteHabitModal = new bootstrap.Modal(
  document.getElementById("delete-habit-modal")
);
if (deleteHabitModal) {
  deleteHabitModal._element.addEventListener("show.bs.modal", (event) => {
    var button = event.relatedTarget;

    var habitName = button.getAttribute("data-habit-name");
    var habitId = button.getAttribute("data-habit-id");

    const deleteBtn =
      deleteHabitModal._element.querySelector("#delete-habit-btn");
    const deleteHabitModaltext = deleteHabitModal._element.querySelector(
      "#delete-habit-modal-text"
    );

    deleteHabitModaltext.textContent = `Completely remove a habit "${habitName}" from the habit tracker. This cannot be undone.`;
    deleteBtn.setAttribute("data-habit-id", habitId);
  });
}

const deleteHabitBtn = document.querySelector("#delete-habit-btn");
deleteHabitBtn.addEventListener("click", deleteHabit);

async function deleteHabit(event) {
  var habitId = deleteHabitBtn.getAttribute("data-habit-id");

  const response = await sendRequestDeleteHabit(habitId);
  if (response.ok) {
    deleteHabitModal.hide();
    await renderTable();
    alert("The habit has been deleted");
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck-create-habit").innerHTML =
        err["detail"];
    });
  }
}

// ================================================================================================================================

// create note modal

// ================================================================================================================================

async function sendRequestCreateNote(data) {
  return await fetch(window.location.origin + "/api/v1/notes/", {
    method: "POST",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
    body: data,
  });
}

const createNoteForm = document.getElementById("create-note-form");
createNoteForm.addEventListener("submit", createNoteFormSubmit);

async function createNoteFormSubmit(event) {
  event.preventDefault();
  button = document.getElementById("create-note-btn");

  const data = formDataToJSON(createNoteForm);

  const response = await sendRequestCreateNote(JSON.stringify(data));
  if (response.ok) {
    clearFormInModal(createNoteModalWindow._element);
    createNoteModalWindow.hide();
    await renderNoteDiv();
    alert("The note has been created");
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck-create-note").innerHTML =
        err["detail"];
    });
  }
}

const createNoteModalWindow = new bootstrap.Modal(
  document.getElementById("create-note-modal")
);
if (createNoteModalWindow) {
  createNoteModalWindow._element.addEventListener("show.bs.modal", () => {
    const createdAtInput =
      createNoteModalWindow._element.querySelector("#note-created-at");

    createdAtInput.value = date.toISOString().substring(0, 10);
  });
}

// ================================================================================================================================

// delete note modal

// ================================================================================================================================

async function sendRequestDeleteNote(note_id) {
  return await fetch(window.location.origin + `/api/v1/notes/${note_id}`, {
    method: "DELETE",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
  });
}

const deleteNoteModal = new bootstrap.Modal(
  document.getElementById("delete-note-modal")
);
if (deleteNoteModal) {
  deleteNoteModal._element.addEventListener("show.bs.modal", (event) => {
    var button = event.relatedTarget;
    var noteId = button.getAttribute("data-note-id");

    const deleteBtn =
      deleteNoteModal._element.querySelector("#delete-note-btn");

    deleteBtn.setAttribute("data-note-id", noteId);
  });
}

const deleteNoteBtn = document.querySelector("#delete-note-btn");
deleteNoteBtn.addEventListener("click", deleteNote);

async function deleteNote() {
  var noteId = deleteNoteBtn.getAttribute("data-note-id");

  const response = await sendRequestDeleteNote(noteId);
  if (response.ok) {
    await renderNoteDiv();
    deleteNoteModal.hide();
    alert("The habit has been deleted");
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck-create-habit").innerHTML =
        err["detail"];
    });
  }
}

// ================================================================================================================================

// edit note modal

// ================================================================================================================================

async function sendRequestPatchNote(data, noteId) {
  return await fetch(window.location.origin + `/api/v1/notes/${noteId}`, {
    method: "PATCH",
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
    body: data,
  });
}

const editNoteForm = document.getElementById("edit-note-form");
editNoteForm.addEventListener("submit", editNoteFormSubmit);

const editNoteModalWindow = new bootstrap.Modal(
  document.getElementById("edit-note-modal")
);
if (editNoteModalWindow) {
  editNoteModalWindow._element.addEventListener("show.bs.modal", (event) => {
    const button = event.relatedTarget;
    var cardDiv = button.closest("div.card");

    var noteId = button.getAttribute("data-note-id");
    var noteText = cardDiv.querySelector(
      "span.text-body-secondary "
    ).textContent;
    var createdAt = cardDiv
      .querySelector("div.card-header")
      .querySelector("span")
      .getAttribute("data-created-at");

    const createdAtInput =
      editNoteModalWindow._element.querySelector("#note-created-at");
    const submitBtn =
      editNoteModalWindow._element.querySelector("#edit-note-btn");
    const textInput = editNoteModalWindow._element.querySelector("#note-text");

    createdAtInput.value = createdAt;
    submitBtn.setAttribute("data-note-id", noteId);
    textInput.value = noteText;
  });
}

async function editNoteFormSubmit(event) {
  event.preventDefault();
  console.log(editNoteForm);
  const button = document.getElementById("edit-note-btn");

  const data = formDataToJSON(editNoteForm);
  const noteId = button.getAttribute("data-note-id");
  console.log(noteId);
  const response = await sendRequestPatchNote(JSON.stringify(data), noteId);
  if (response.ok) {
    editNoteModalWindow.hide();
    await renderNoteDiv();
    alert("The note has been edited");
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck-create-note").innerHTML =
        err["detail"];
    });
  }
}

// ================================================================================================================================

// clear forms function

// ================================================================================================================================

function clearFormInModal(modal) {
  let invalidFeedbackDiv = modal.querySelector(".invalid-feedback-my");
  let inputs = modal.querySelectorAll("input");
  let textArea = modal.querySelector("textarea");

  if (textArea !== null) {
    textArea.value = "";
  }
  inputs.forEach((input) => (input.value = ""));
  invalidFeedbackDiv.textContent = "";
}
