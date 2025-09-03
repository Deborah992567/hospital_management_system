async function loadMedicines() {
  const res = await fetch(`${API_BASE}/pharmacy/`, { headers: getAuthHeaders() });
  const meds = await res.json();

  const tbody = document.getElementById("medicinesTable");
  tbody.innerHTML = "";
  meds.forEach(m => {
    tbody.innerHTML += `
      <tr>
        <td>${m.id}</td>
        <td>${m.name}</td>
        <td>${m.stock}</td>
        <td>${m.price}</td>
      </tr>
    `;
  });
}

document.getElementById("medicineForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    name: document.getElementById("name").value,
    stock: parseInt(document.getElementById("stock").value),
    price: parseFloat(document.getElementById("price").value),
    expiry_date: document.getElementById("expiry_date").value
  };

  const res = await fetch(`${API_BASE}/pharmacy/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    loadMedicines();
  } else {
    alert("Failed to add medicine");
  }
});

loadMedicines();
