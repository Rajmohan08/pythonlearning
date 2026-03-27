const statusEl = document.getElementById('status');
const itemsEl = document.getElementById('items');
const formEl = document.getElementById('item-form');
const nameEl = document.getElementById('name');
const descriptionEl = document.getElementById('description');

async function fetchItems() {
  statusEl.textContent = 'Loading...';
  try {
    const response = await fetch('/api/items');
    if (!response.ok) {
      throw new Error('API error');
    }
    const items = await response.json();
    renderItems(items);
    statusEl.textContent = items.length ? '' : 'No items yet.';
  } catch (error) {
    statusEl.textContent = 'Unable to load items.';
  }
}

function renderItems(items) {
  itemsEl.innerHTML = '';
  items.forEach((item) => {
    const li = document.createElement('li');
    li.className = 'item';
    li.innerHTML = `<strong>${item.name}</strong><span>${item.description || ''}</span>`;
    itemsEl.appendChild(li);
  });
}

formEl.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = {
    name: nameEl.value.trim(),
    description: descriptionEl.value.trim() || null,
  };

  if (!payload.name) {
    return;
  }

  try {
    const response = await fetch('/api/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error('API error');
    }

    nameEl.value = '';
    descriptionEl.value = '';
    await fetchItems();
  } catch (error) {
    statusEl.textContent = 'Unable to save item.';
  }
});

fetchItems();
