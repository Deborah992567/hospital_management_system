async function loadAppointments() {
  const res = await fetch(`${API_BASE}/appointments/`, { headers: getAuthHeaders() });
  const appointments = await res.json();

  const tbody = document.getElementById("appointmentsTable");
  tbody.innerHTML = "";
  appointments.forEach(a => {
    tbody.innerHTML += `
      <tr>
        <td>${a.id}</td>
        <td>${a.patient_id}</td>
        <td>${a.doctor_id}</td>
        <td>${a.date_time}</td>
        <td>${a.status}</td>
      </tr>
    `;
  });
}

document.getElementById("appointmentForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    patient_id: parseInt(document.getElementById("patient_id").value),
    doctor_id: parseInt(document.getElementById("doctor_id").value),
    date_time: document.getElementById("date_time").value,
    note: document.getElementById("note").value
  };

  const res = await fetch(`${API_BASE}/appointments/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    loadAppointments();
  } else {
    alert("Failed to book appointment");
  }
});

loadAppointments();
