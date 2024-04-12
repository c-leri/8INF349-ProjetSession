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
  orders.orders = [];
};

// === Observers ===

sidebarToggle.observe((property, value) => {
  if (property === "open") {
    if (value) {
      containerElement.dataset.sidebarOpen = "";
      buyButton.tabIndex = 0;
    } else {
      delete containerElement.dataset.sidebarOpen;
      buyButton.tabIndex = -1;
    }
  }
});

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
  if (property === "orders") {
    if (value.length > 0) {
      ordersElement.replaceChildren(
        ...value
          .sort((a, b) => a.id - b.id)
          .map((order) => shortOrderToView(order))
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
  sidebarToggle.open = !sidebarToggle.open;
};

buyButton.onclick = async () => {
  buyButton.disabled = true;

  let success = await postOrder();

  if (success) personalInformationsDialog.showModal();
  else buyButton.disabled = false;
};

personalInformationsDialog.onclose = () => {
  personalInformationsForm.reset();
};

personalInformationsForm.onsubmit = async (event) => {
  event.preventDefault();

  let success = await putPersonalInformations(
    new FormData(personalInformationsForm)
  );

  if (success) {
    personalInformationsDialog.close();
    creditCardDialog.showModal();
  }
};

creditCardDialog.onclose = () => {
  creditCardForm.reset();
};

creditCardForm.onsubmit = async (event) => {
  event.preventDefault();

  let success = await putCreditCard(new FormData(creditCardForm));

  if (success) {
    creditCardDialog.close();
  }
};

closeOrderRecapButton.onclick = () => {
  orderRecapDialog.close();
};
