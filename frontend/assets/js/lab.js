async function loadLabTests() {
  const res = await fetch(`${API_BASE}/lab/tests`, { headers: getAuthHeaders() });
  const tests = await res.json();

  const tbody = document.getElementById("labTestsTable");
  tbody.innerHTML = "";
  tests.forEach(t => {
    tbody.innerHTML += `
      <tr>
        <td>${t.id}</td>
        <td>${t.name}</td>
        <td>${t.description || "-"}</td>
      </tr>
    `;
  });
}

document.getElementById("labTestForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value
  };

  const res = await fetch(`${API_BASE}/lab/tests`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    loadLabTests();
  } else {
    alert("Failed to add test");
  }
});

loadLabTests();
