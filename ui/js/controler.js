window.onload = () => {
  products.observe((property, value) => {
    if (property == "products" && value != []) {
      productsElement.append(
        ...value
          .sort((a, b) => a.id - b.id)
          .map((product) => productToView(product))
      );
    }
  });

  loadProducts();
};

sidebarToggleButton.onclick = () => {
  if (containerElement.dataset.sidebarOpen === "")
    delete containerElement.dataset.sidebarOpen;
  else containerElement.dataset.sidebarOpen = "";
};
