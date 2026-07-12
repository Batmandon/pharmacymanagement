// async function navigate() {
//     const supplier = document.querySelector(".supplier");
//     supplier.addEventListener("click", async(event) => {
//         event.preventDefault();
//         Swal.fire ({
//             icon: "error",
//             title: "Work under way"
//         })
//     })
//     const setting = document.querySelector(".setting");
//     setting.addEventListener("click", async(event) => {
//         event.preventDefault();
//         Swal.fire ({
//             icon: "error",
//             title: "Work under way"
//         })
//     })

//     const history = document.querySelector(".history");
//     history.addEventListener("click", async(event) => {
//         console.log(event)
//         event.preventDefault();
//         window.location.href = "order_history.html"
//     })

//     const order = document.querySelector(".order");
//     order.addEventListener("click", async(event) =>{
//         event.preventDefault();
//         window.location.href = "orders.html"
//     })

//     const inventory = document.querySelector(".inventory");
//     inventory.addEventListener("click", async(event) =>{
//         event.preventDefault();
//         window.location.href = "dashboard.html"
//     })
// }
// async function navigate(location) {
//     const history = document.querySelector(location);
//     location.addEventListener("click", async(event) => {
//         console.log(event)
//         event.preventDefault();

//         if (location === "order")
//         window.location.href = "order_history.html"
//     })
// }



async function navigate() {
    const ul = document.querySelector("ul");
    ul.addEventListener("click", async (event) => {
        const clas = event.target.className
        const element = event.target
        console.log(clas)

        if (clas === "setting") {
            event.preventDefault();
            Swal.fire({
                icon: "error",
                title: "Work under way"
            });
        } else if (clas === "supplier") {
            event.preventDefault();
            Swal.fire({
                icon: "error",
                title: "Work under way"
            });
        } else if (clas === "history") {
            event.preventDefault();
            window.location.href = "../order/order_history.html";
        } else if (clas === "order") {
            event.preventDefault();
            window.location.href = "../order/orders.html";
        } else if (clas === "inventory") {
            event.preventDefault();
            window.location.href = "../dashboard/dashboard.html";
        }
    })
}

navigate()
export { navigate };


// const active = document.querySelector(".active");
// const order = document.querySelector(".order");
// active.classList.remove('active');
// order.classList.add('active');