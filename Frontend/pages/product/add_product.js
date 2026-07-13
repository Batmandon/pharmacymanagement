document.getElementById("save-products").addEventListener("click", async (event) => {
    event.preventDefault();

    // Get ALL rows from the table body
    const rows = document.querySelectorAll("#table-body tr");

    const productData = [];

    rows.forEach(row => {
        const inputs = row.querySelectorAll("input");

        // inputs[0] = medicine_name, [1] = batch_no, [2] = expiry_date, [3] = quantity, [4] = price
        productData.push({
            medicine_name: inputs[0].value,
            batch_no: inputs[1].value,
            expiry_date: inputs[2].value,
            quantity: parseInt(inputs[3].value),
            price: parseInt(inputs[4].value)
        });
    });

    console.log("Sending products:", productData);

    const response = await fetch(`${API_BASE_URL}/addproducts`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(productData)  // sending a LIST now
    });

    const data = await response.json();

    if (response.ok) {
        console.log("Products added successfully:", data);
        Swal.fire({
            icon: "success",
            title: "Products Added",
            text: "All products have been added successfully!"
        });
    } else {
        console.error("Failed:", data);
        Swal.fire({
            icon: "error",
            title: "Failed to Add Product",
            text: data.error || "An error occurred"
        });
    }
});


