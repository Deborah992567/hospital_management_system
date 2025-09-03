async function loadPatients() {
  const res = await fetch(`${API_BASE}/patients/`, { headers: getAuthHeaders() });
  const patients = await res.json();

  const tbody = document.getElementById("patientsTable");
  tbody.innerHTML = "";
  patients.forEach(p => {
    tbody.innerHTML += `
      <tr>
        <td>${p.id}</td>
        <td>${p.name}</td>
        <td>${p.dob || "-"}</td>
        <td>${p.gender || "-"}</td>
        <td>${p.contact || "-"}</td>
      </tr>
    `;
  });
}

document.getElementById("patientForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    name: document.getElementById("name").value,
    dob: document.getElementById("dob").value,
    gender: document.getElementById("gender").value,
    contact: document.getElementById("contact").value,
    address: document.getElementById("address").value
  };

  const res = await fetch(`${API_BASE}/patients/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    loadPatients();
    document.querySelector("#addPatientModal .btn-close")?.click();
  } else {
    alert("Failed to add patient");
  }
});

loadPatients();
