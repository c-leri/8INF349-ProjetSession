window.onload = () => {
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
};

sidebarToggleButton.onclick = () => {
  if (containerElement.dataset.sidebarOpen === "")
    delete containerElement.dataset.sidebarOpen;
  else containerElement.dataset.sidebarOpen = "";
};

cart.observe((property, value) => {
  if (property === "items") {
    if (value.length > 0) {
      cartItemsElement.replaceChildren(
        ...value.sort((a, b) => a.id - b.id).map((item) => cartItemToView(item))
      );
    } else {
      let emptyCart = document.createElement("p");
      emptyCart.textContent = "Your cart is empty.";
      emptyCart.classList.add("empty");
      cartItemsElement.replaceChildren(emptyCart);
    }
  }
});
