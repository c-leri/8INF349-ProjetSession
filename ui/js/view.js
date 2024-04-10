// === Elements ===

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
let ordersElement = document.getElementById("orders");

/**
 * @type {HTMLDivElement}
 */
let containerElement = document.getElementById("container");

/**
 * @type {HTMLDivElement}
 */
let productsElement = document.getElementById("products");

/**
 * @type {HTMLDialogElement}
 */
let personalInformationsDialog = document.getElementById(
  "personal-informations"
);

/**
 * @type {HTMLFormElement}
 */
let personalInformationsForm = document.querySelector(
  "#personal-informations form"
);

/**
 * @type {HTMLDialogElement}
 */
let creditCardDialog = document.getElementById("credit-card");

/**
 * @type {HTMLFormElement}
 */
let creditCardForm = document.querySelector("#credit-card form");

/**
 * @type {HTMLDialogElement}
 */
let orderRecapDialog = document.getElementById("order-recap");

// === Icons ===

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
 * @type {SVGElement}
 */
let openIcon = document.getElementById("open-icon");

/**
 * @type {SVGElement}
 */
let checkCircleIcon = document.getElementById("check-circle-icon");

/**
 * @type {SVGElement}
 */
let xCircleIcon = document.getElementById("x-circle-icon");

// === View Generation ===

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

  sidebarToggle.observe((property, value) => {
    if (property === "open") {
      if (value) {
        minus.tabIndex = 0;
        plus.tabIndex = 0;
      } else {
        minus.tabIndex = -1;
        plus.tabIndex = -1;
      }
    }
  });

  let root = document.createElement("div");
  root.classList.add("cart-item");
  root.append(name, minus, count, plus);

  return root;
}

/**
 * @param {ShortOrder} order
 * @returns {HTMLDivElement}
 */
function shortOrderToView(order) {
  let name = document.createElement("p");
  name.classList.add("name");
  name.textContent = `Order ${order.id}`;

  let paidBadge = document.createElement("div");
  paidBadge.classList.add("paid-badge");
  paidBadge.appendChild(
    order.paid ? checkCircleIcon.cloneNode(true) : xCircleIcon.cloneNode(true)
  );

  let openRecapButton = document.createElement("button");
  openRecapButton.classList.add("open-recap");
  openRecapButton.appendChild(openIcon.cloneNode(true));
  openRecapButton.onclick = async () => {
    openOrderRecap(await getOrder(order.id));
  };

  sidebarToggle.observe((property, value) => {
    if (property === "open") {
      if (value) openRecapButton.tabIndex = 0;
      else openRecapButton.tabIndex = -1;
    }
  });

  let root = document.createElement("div");
  root.classList.add("order");
  if (order.paid) root.dataset.paid = "";
  root.append(name, paidBadge, openRecapButton);

  return root;
}

/**
 * @param {Order} order
 */
function openOrderRecap(order) {
  let todo = orderRecapDialog.querySelector("div.todo");

  todo.textContent = JSON.stringify(order);

  orderRecapDialog.showModal();
}
