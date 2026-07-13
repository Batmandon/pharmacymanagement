// import { checkAuth } from './auth.js';

// checkAuth();

// import { navigate } from './navigate.js';
// navigate();

const total = document.querySelector(".stat-card .total")
const low_stock = document.querySelector(".stat-card .low-stock")
const expiry = document.querySelector(".stat-card .expiry")

document.getElementById("add-product").addEventListener("click", async (event) => {
    event.preventDefault();
    console.log("Add Product button clicked");
    window.location.href = "../product/add_product.html";
});

async function fetchProducts() {
    const response = await fetch(`${API_BASE_URL}/getproduct`, {
        method: "GET",
        credentials: "include"
    });

    const products = await response.json();
    total.textContent = products.length

    let low = 0;
    products.forEach(product => {
        if (product.quantity <= 10) {
            low++;
        }
    })
    low_stock.textContent = low;

    let count = 0;
    products.forEach(product => {
        if (product.expiry_status.includes("expiring") || product.expiry_status.includes("expired")) {
            count++;
        }
    })
    expiry.textContent = count;

    const tbody = document.querySelector(".product-body");
    let prodid = 0; // Initialize the ID counter
    if (products.length > 0) {
        tbody.innerHTML = "";
        products.forEach(product => {
            prodid += 1; // Increment the ID counter for each product
            const row = document.createElement("tr");

            row.innerHTML = `
            <td>${prodid}</td>
            <td>${product.medicine_name}</td>
            <td>${product.batch_no}</td>
            <td>${product.expiry_date}</td>
            <td>${product.price}</td>
            <td>${product.quantity}</td>
            <td class="expiry_status">${product.expiry_status}</td>
            <td><button class="btn btn-primary edit-product" data-id="${product.id}">Edit</button></td>
            <td><button class="btn btn-danger delete-product" data-id="${product.id}">Delete</button></td>
        `;
            tbody.appendChild(row);

        });
    } else {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 6;
        cell.textContent = "No products available";
        row.appendChild(cell);
        tbody.appendChild(row);

    }

}

fetchProducts();

async function expiry_status() {
    const response = await fetch(`${API_BASE_URL}/expiryproduct`, {
        method: "PATCH",
        credentials: "include"
    });

    const expiry_status = await response.json();
    // if (response.ok) {
    //     console.log("Expiry status", expiry_status)
    // } else {
    //     console.error("Failed to get expiry status")
    // }

    const expiry = document.querySelectorAll('.expiry_status');
    expiry.forEach((exp) => {
        if (exp.textContent === "safe") {
            exp.classList.add("safe")
        } else if (exp.textContent === "expired") {
            exp.classList.add("expired")
        } else {
            exp.classList.add("expiring")
        }
        // console.log(expiry)
    });
}

expiry_status();

async function deleteProduct() {
    const tbody = document.querySelector(".product-body");
    tbody.addEventListener("click", async (event) => {
        if (event.target.classList.contains("delete-product")) {
            const productId = event.target.getAttribute('data-id'); // Get product ID directly from clicked button
            console.log("Delete button clicked for product ID:", productId);
            const result = await swal.fire({
                text: 'Are you sure you want to delete this product?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel'
            });
            if (result.isConfirmed) {
                try {
                    const response = await fetch(`${API_BASE_URL}/delete/${productId}`, {
                        method: "DELETE",
                        credentials: "include"
                    });
                    if (response.ok) {
                        console.log("Product deleted successfully");
                        fetchProducts(); // Refresh the product list
                    } else {
                        console.error("Failed to delete product");
                    }
                } catch (error) {
                    console.error("Error deleting product:", error);
                }
            }
        }
    });
}

deleteProduct();

async function editProduct() {
    const tbody = document.querySelector(".product-body");

    tbody.addEventListener("click", (event) => {
        const productId = event.target.getAttribute('data-id'); // Get product ID directly from clicked button
        console.log("Edit button clicked for product ID:", productId);

        if (!event.target.classList.contains("edit-product")) {
            return; // Exit if the clicked element is not an edit button
        }

        const row = event.target.closest("tr")
        if (!row) return;

        const cells = Array.from(row.querySelectorAll("td")).slice(1, -2); // Exclude the first and last two cells (ID and buttons)

        const editRow = document.createElement("tr");

        const inputs = cells.map(cell => {
            const td = document.createElement("td");
            const input = document.createElement("input");
            input.value = cell.textContent.trim();
            td.appendChild(input);
            editRow.appendChild(td);
            return input;
        });

        tbody.replaceChild(editRow, row);

        editRow.addEventListener("keypress", (event) => {
            if (event.key === "Enter") {
                console.log("Enter key pressed, updating product");

                cells.forEach((cell, i) => {
                    cell.textContent = inputs[i].value;
                });
                tbody.replaceChild(row, editRow);

                const updatedProduct = {
                    medicine_name: inputs[0].value,
                    batch_no: inputs[1].value,
                    expiry_date: inputs[2].value,
                    price: inputs[3].value,
                    quantity: inputs[4].value
                };

                const response = fetch(`${API_BASE_URL}/update/${productId}`, {
                    method: "PATCH",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(updatedProduct)
                });
                console.log("Product updated successfully:", updatedProduct);
            }

        });
    });
}
editProduct();

const active = document.querySelector(".active");
const inventory = document.querySelector(".inventory");
active.classList.remove('active');
inventory.classList.add('active');
