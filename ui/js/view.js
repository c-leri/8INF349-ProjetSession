/**
 * @type {HTMLDivElement}
 */
let productsElement = document.getElementById("products");

/**
 * @param {Product} product
 * @returns {HTMLDivElement}
 */
function productToView(product) {
  let name = document.createElement("p");
  name.classList.add("name");
  name.textContent = product.name;

  let description = document.createElement("p");
  description.classList.add("description");
  description.textContent = product.description;

  let price = document.createElement("p");
  price.classList.add("price");
  price.textContent = `${product.price} $`;

  let in_stock = document.createElement("p");
  in_stock.classList.add("stock");
  in_stock.dataset.inStock = product.in_stock;
  in_stock.textContent = product.in_stock ? "In Stock" : "Out Of Stock";

  let root = document.createElement("div");
  root.classList.add("product");
  root.dataset.id = product.id;
  root.append(name, description, price, in_stock);

  return root;
}
