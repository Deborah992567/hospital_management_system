async function loadBills() {
  const res = await fetch(`${API_BASE}/billing/`, { headers: getAuthHeaders() });
  const bills = await res.json();

  const tbody = document.getElementById("billsTable");
  tbody.innerHTML = "";
  bills.forEach(b => {
    tbody.innerHTML += `
      <tr>
        <td>${b.id}</td>
        <td>${b.patient_id}</td>
        <td>${b.amount}</td>
        <td>${b.status}</td>
        <td>${b.created_at}</td>
      </tr>
    `;
  });
}

document.getElementById("billForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    patient_id: parseInt(document.getElementById("patient_id").value),
    amount: parseFloat(document.getElementById("amount").value),
    description: document.getElementById("description").value
  };

  const res = await fetch(`${API_BASE}/billing/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    loadBills();
  } else {
    alert("Failed to create bill");
  }
});

loadBills();
