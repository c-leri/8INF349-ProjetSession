// === Setup ===
window.onload = () => {
  // Display the products
  products.observe((property, value) => {
    if (property === "products") {
      if (value.length > 0) {
        productsElement.append(
          ...value
            .sort((a, b) => a.id - b.id)
            .map((product) => productToView(product))
        );
      } else {
        let emptyProducts = document.createElement("p");
        emptyProducts.textContent = "The products failed to load.";
        emptyProducts.classList.add("empty");
        productsElement.replaceChildren(emptyProducts);
      }
    }
  });

  loadProducts();

  cart.items = [];
  orders.orderIds = [];
};

// === Observers ===

// Display the cart content
cart.observe((property, value) => {
  if (property === "items") {
    if (value.length > 0) {
      cartItemsElement.replaceChildren(
        ...value.sort((a, b) => a.id - b.id).map((item) => cartItemToView(item))
      );

      buyButton.disabled = false;
    } else {
      let emptyCart = document.createElement("p");
      emptyCart.textContent = "Your cart is empty.";
      emptyCart.classList.add("empty");
      cartItemsElement.replaceChildren(emptyCart);

      buyButton.disabled = true;
    }
  }
});

// Display the order list
orders.observe((property, value) => {
  if (property === "orderIds") {
    if (value.length > 0) {
      ordersElement.replaceChildren(
        ...value.sort((a, b) => a - b).map((orderId) => orderIdToView(orderId))
      );
    } else {
      let emptyOrders = document.createElement("p");
      emptyOrders.textContent = "You haven't bought anything yet.";
      emptyOrders.classList.add("empty");
      ordersElement.replaceChildren(emptyOrders);
    }
  }
});

// === Event Listener ===

sidebarToggleButton.onclick = () => {
  if (containerElement.dataset.sidebarOpen === "")
    delete containerElement.dataset.sidebarOpen;
  else containerElement.dataset.sidebarOpen = "";
};

buyButton.onclick = async () => {
  let success = await postOrder();

  if (success) personalInformationsDialog.showModal();
};

personalInformationsForm.onsubmit = async (event) => {
  event.preventDefault();

  let success = await putPersonalInformations(
    new FormData(personalInformationsForm)
  );

  if (success) {
    personalInformationsDialog.close();
    personalInformationsForm.reset();
    creditCardDialog.showModal();
  }
};

creditCardForm.onsubmit = async (event) => {
  event.preventDefault();

  let success = await putCreditCard(new FormData(creditCardForm));

  if (success) {
    creditCardDialog.close();
    creditCardForm.reset();
  }
};
