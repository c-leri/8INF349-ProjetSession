/**
 * @type {HTMLButtonElement}
 */
let sidebarToggleButton = document.querySelector("nav button");

/**
 * @type {HTMLDivElement}
 */
let cartItemsElement = document.getElementById("cart-items");

/**
 * @type {HTMLButtonElement}
 */
let buyButton = document.getElementById("buy");

/**
 * @type {HTMLDivElement}
 */
let containerElement = document.getElementById("container");

/**
 * @type {HTMLDivElement}
 */
let productsElement = document.getElementById("products");

// Icons

/**
 * @type {SVGElement}
 */
let addToCartIcon = document.getElementById("add-to-cart-icon");

/**
 * @type {SVGElement}
 */
let plusIcon = document.getElementById("plus-icon");

/**
 * @type {SVGElement}
 */
let minusIcon = document.getElementById("minus-icon");

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

  let stock = document.createElement("p");
  stock.classList.add("stock");
  if (product.in_stock) stock.dataset.inStock = "";
  stock.textContent = product.in_stock ? "In Stock" : "Out Of Stock";

  let addToCartButton = document.createElement("button");
  addToCartButton.classList.add("add-to-cart");
  addToCartButton.appendChild(addToCartIcon.cloneNode(true));
  addToCartButton.disabled = !product.in_stock;
  addToCartButton.onclick = () => addToCart(product.id);

  let root = document.createElement("div");
  root.classList.add("product");
  root.append(name, description, price, stock, addToCartButton);

  return root;
}

/**
 * @param {CartItem} cartItem
 * @returns {HTMLDivElement}
 */
function cartItemToView(cartItem) {
  let name = document.createElement("p");
  name.classList.add("name");
  name.textContent = products.products.find(
    (product) => product.id === cartItem.id
  ).name;

  let minus = document.createElement("button");
  minus.classList.add("minus");
  minus.appendChild(minusIcon.cloneNode(true));
  minus.onclick = () => removeFromCart(cartItem.id);

  let count = document.createElement("p");
  count.classList.add("count");
  count.textContent = cartItem.count;

  let plus = document.createElement("button");
  plus.classList.add("plus");
  plus.appendChild(plusIcon.cloneNode(true));
  plus.onclick = () => addToCart(cartItem.id);

  let root = document.createElement("div");
  root.classList.add("cart-item");
  root.append(name, minus, count, plus);

  return root;
}
