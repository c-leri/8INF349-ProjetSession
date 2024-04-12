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
  "personal-information"
);

/**
 * @type {HTMLFormElement}
 */
let personalInformationsForm = document.querySelector(
  "#personal-information form"
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

/**
 * @type {HTMLButtonElement}
 */
let closeOrderRecapButton = document.getElementById("order-close");

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
  price.textContent = `$${product.price}`;

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
 * @returns {void}
 */
function openOrderRecap(order) {
  let productsElement = orderRecapDialog.querySelector("#order-products");
  productsElement.replaceChildren(
    ...order.products.map((product) => orderProductToView(product))
  );

  let totalPriceElement = orderRecapDialog.querySelector("#order-total-price");
  totalPriceElement.textContent = `$${order.total_price}`;

  let shippingPriceElement = orderRecapDialog.querySelector(
    "#order-shipping-price"
  );
  shippingPriceElement.textContent = `$${order.shipping_price}`;

  if (
    order.email &&
    order.shipping_information &&
    Object.keys(order.shipping_information).length > 0
  ) {
    orderRecapDialog.querySelector(
      "#order-personal-information"
    ).hidden = false;

    let emailElement = orderRecapDialog.querySelector("#order-email");
    emailElement.textContent = order.email;

    let addressElement = orderRecapDialog.querySelector("#order-address");
    addressElement.textContent = order.shipping_information.address;

    let postalCodeElement =
      orderRecapDialog.querySelector("#order-postal-code");
    postalCodeElement.textContent = order.shipping_information.postal_code;

    let cityElement = orderRecapDialog.querySelector("#order-city");
    cityElement.textContent = order.shipping_information.city;

    let provinceElement = orderRecapDialog.querySelector("#order-province");
    provinceElement.textContent = order.shipping_information.province;

    let countryElement = orderRecapDialog.querySelector("#order-country");
    countryElement.textContent = order.shipping_information.country;
  } else {
    orderRecapDialog.querySelector("#order-personal-information").hidden = true;
  }

  if (order.credit_card && Object.keys(order.credit_card).length > 0) {
    orderRecapDialog.querySelector("#order-credit-card").hidden = false;

    let creditCardNameElement = orderRecapDialog.querySelector(
      "#order-credit-card-name"
    );
    creditCardNameElement.textContent = order.credit_card.name;

    let creditCardNumberElement = orderRecapDialog.querySelector(
      "#order-credit-card-number"
    );
    creditCardNumberElement.textContent = `${order.credit_card.first_digits}...${order.credit_card.last_digits}`;

    let creditCardExpirationElement = orderRecapDialog.querySelector(
      "#order-credit-card-expiration"
    );
    creditCardExpirationElement.textContent = `${(
      "0" + order.credit_card.expiration_month
    ).slice(-2)}/${order.credit_card.expiration_year}`;
  } else {
    orderRecapDialog.querySelector("#order-credit-card").hidden = true;
  }

  if (order.transaction && Object.keys(order.transaction).length > 0) {
    orderRecapDialog.querySelector("#order-transaction").hidden = false;

    let transactionSuccessElement = orderRecapDialog.querySelector(
      "#order-transaction-success"
    );
    transactionSuccessElement.replaceChildren(
      order.transaction.success
        ? checkCircleIcon.cloneNode(true)
        : xCircleIcon.cloneNode(true)
    );

    if (order.transaction.success) {
      transactionSuccessElement.dataset.success = "";

      orderRecapDialog.querySelector(
        "#order-transaction-id-container"
      ).hidden = false;
      orderRecapDialog.querySelector("#order-transaction-error").hidden = true;

      let transactionIdElement = orderRecapDialog.querySelector(
        "#order-transaction-id"
      );
      transactionIdElement.textContent = order.transaction.id;
    } else {
      delete transactionSuccessElement.dataset.success;

      orderRecapDialog.querySelector(
        "#order-transaction-id-container"
      ).hidden = true;
      orderRecapDialog.querySelector("#order-transaction-error").hidden = false;

      let transactionErrorCodeElement = orderRecapDialog.querySelector(
        "#order-transaction-error-code"
      );
      transactionErrorCodeElement.textContent = order.transaction.error.code;

      let transactionErrorNameElement = orderRecapDialog.querySelector(
        "#order-transaction-error-name"
      );
      transactionErrorNameElement.textContent = order.transaction.error.name;
    }

    let transactionAmountChargedElement = orderRecapDialog.querySelector(
      "#order-transaction-amount-charged"
    );
    transactionAmountChargedElement.textContent = `$${order.transaction.amount_charged}`;
  } else {
    orderRecapDialog.querySelector("#order-transaction").hidden = true;
  }

  orderRecapDialog.showModal();
}

/**
 * @param {OrderProduct} orderProduct
 * @returns {HTMLDivElement}
 */
function orderProductToView(orderProduct) {
  let product = products.products.find(
    (product) => product.id === orderProduct.id
  );

  let name = document.createElement("p");
  name.classList.add("name");
  name.textContent = product.name;

  let quantity = document.createElement("p");
  quantity.classList.add("quantity");
  quantity.textContent = `x${orderProduct.quantity}`;

  let price = document.createElement("p");
  price.classList.add("price");
  price.textContent = `$${(product.price * orderProduct.quantity).toFixed(2)}`;

  let root = document.createElement("div");
  root.classList.add("product");
  root.append(name, quantity, price);

  return root;
}
