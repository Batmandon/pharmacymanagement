async function logOrder() {
    try {
        const response = await fetch(`${API_BASE_URL}/orderhistory`, {
            method: "GET",
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const orders = await response.json();
        const bar = document.querySelector(".topbar");
        const tbody = document.querySelector("#table");


        if (!bar || !tbody) {
            return;
        }

        tbody.innerHTML = "";

        if (!Array.isArray(orders) || orders.length === 0) {
            tbody.innerHTML = "<tr><td colspan='2'>No orders have been sent</td></tr>";
            return;
        }

        const header = document.createElement("h3");
        header.classList.add("sender")
        header.textContent = `${"Orders sent via WhatsApp"}`;
        bar.appendChild(header);

        orders.forEach((order, index) => {
            if (!Array.isArray(order.items) || order.items.length === 0) {
                const row = document.createElement("tr");
                row.innerHTML = "<td colspan='2'>No items in this order</td>";
                tbody.appendChild(row);
                return;
            }

            order.items.forEach((item) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.medicine_name || "Unknown medicine"}</td>
                    <td>${item.quantity ?? 0}</td>
                `;
                tbody.appendChild(row);
            });
        });
    } catch (error) {
        console.error("Failed to load order history:", error);
        const tbody = document.querySelector("#table");
        if (tbody) {
            tbody.innerHTML = "<tr><td colspan='2'>Unable to load order history</td></tr>";
        }
    }
}

logOrder();

const active = document.querySelector(".active");
const history = document.querySelector(".history");
active.classList.remove('active');
history.classList.add('active');