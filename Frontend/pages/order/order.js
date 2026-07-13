let ordersToSend = [];

// Post order to the server
async function addOrder() {
    const response = await fetch(`${API_BASE_URL}/addorder`, {
        method: "POST",
        credentials: "include"
    });

    const addorder = await response.json();
    console.log("Order:", addorder)
}
await addOrder();
// fetch order from the server and display in the table
async function fetchOrder() {
    const response = await fetch(`${API_BASE_URL}/getorder`, {
        method: "GET",
        credentials: "include"
    });

    const orders = await response.json();
    ordersToSend = orders;
    console.log("ordersToSend:", ordersToSend); // Store the fetched orders in the global variable
    console.log(orders);
    const tbody = document.querySelector("#table");
    const orderqty = 20;
    let orderid = 0;
    if (orders.length > 0) {
        tbody.innerHTML = "";
        orders.forEach(order => {
            orderid += 1;
            const row = document.createElement("tr");
            row.innerHTML = `
            <td>${orderid}</td>
            <td>${order.medicine_name}</td>
            <td class="low-stock">${order.current_stock}</td>
            <td> <input type="number" value="${order.quantity}"</input></td>
            <td> <span class="status status-pending">${order.status}</span></td>
        `;
            tbody.appendChild(row);
            console.log("Order added to table:", order);
        });

    }
}
await fetchOrder();

// make a function to generate a link to send order to whatsapp
async function sendOrder() {
    const response = await fetch(`${API_BASE_URL}/sendorder`, {
        method: "GET",
        credentials: "include"
    });

    const sendorder = await response.json();
    console.log("Order sent:", sendorder);

    const waLink = sendorder.whatsapp_url || sendorder.url || sendorder.link;
    if (!waLink) {
        console.error("sendOrder: no WhatsApp URL returned from server", sendorder);
        return;
    }
    window.open(waLink, "_blank");
};

async function logOrder(confirmDuplicate) {
    const response = await fetch(`${API_BASE_URL}/orders`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ items: ordersToSend, confirm_duplicate: confirmDuplicate })
    });

    return await response.json();
}

// Post order to the server and send to whatsapp when the button is clicked
document.querySelector(".btn-whatsapp").addEventListener("click", async (event) => {
    event.preventDefault();
    console.log("button clicked");

    const result = await logOrder(false);

    if (result.warning === "duplicate_order") {
        const userConfirmed = await Swal.fire ({
            title: "Duplicate Order",
            text: result.message,
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Yes",
            cancelButtonText: "Cancel"
        });
        
        if (userConfirmed === cancelButtonText) {
            return; // user ne cancel kiya, WhatsApp mat bhejo
        }
        await logOrder(true); // confirm karke dobara log karo
    }

    await sendOrder();
    update_status("Sent");
});

// Navigation of bg color of active link in the sidebar
const active = document.querySelector(".active");
const order = document.querySelector(".order");
active.classList.remove('active');
order.classList.add('active');



const pending = document.querySelector(".pending");
const send = document.querySelector(".send");
async function statcard() {
    let left = 0
    let sent = 0
    const card = document.querySelectorAll(".status").forEach(stat => {
        if (stat.textContent === "Pending") {
            left++;
            stat.classList.remove("status-sent");
            stat.classList.add("status-pending");
        } else {
            sent++;
            stat.classList.remove("status-pending");
            stat.classList.add("status-sent");
        }
    })
    pending.textContent = left;
    send.textContent = sent;
}
statcard();


async function update_status(status) {
    await fetch(`${API_BASE_URL}/update_status/${status}`, {
        method: "PATCH",
        credentials: "include",
        headers: { "Content-Type": "application/json" }
    })
}