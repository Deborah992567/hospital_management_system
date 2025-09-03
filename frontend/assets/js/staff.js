async function loadStaff() {
  const res = await fetch(`${API_BASE}/staff/`, { headers: getAuthHeaders() });
  const staff = await res.json();

  const tbody = document.getElementById("staffTable");
  tbody.innerHTML = "";
  staff.forEach(s => {
    tbody.innerHTML += `
      <tr>
        <td>${s.id}</td>
        <td>${s.name}</td>
        <td>${s.email}</td>
        <td>${s.role}</td>
      </tr>
    `;
  });
}

document.getElementById("staffForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    role: document.getElementById("role").value
  };

  const res = await fetch(`${API_BASE}/staff/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    loadStaff();
  } else {
    alert("Failed to add staff");
  }
});

loadStaff();
