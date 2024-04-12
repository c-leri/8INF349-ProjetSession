/**
 * @type {Observable<{open: boolean}>}
 */
let sidebarToggle = makeObservable({ open: false });

// === API ===

const API_URL = "http://localhost:5000";

/**
 * @type {Observable<Products>}
 */
let products = makeObservable({ products: [] });

/**
 * @type {Observable<{orders: ShortOrder[]}>}
 */
let orders = makeObservable({ orders: [] });

/**
 * @type {number|undefined}
 */
let currentOrderId = undefined;

/**
 * Loads the products from the API into `products`
 * @returns {void}
 */
function loadProducts() {
  fetch(`${API_URL}/`)
    .then((response) => {
      if (!response.ok) return;
      response.json().then((data) => {
        products.products = data.products;
      });
    })
    .catch((err) => console.error(err));
}

/**
 * Send the products in the cart to the API to create an order
 * @returns {Promise<boolean>} false if the request fails in any way
 */
async function postOrder() {
  try {
    let response = await fetch(`${API_URL}/order`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        products: [
          ...cart.items.map((item) => ({ id: item.id, quantity: item.count })),
        ],
      }),
    });

    if (!response.ok || !response.redirected) return false;

    cart.items = [];

    response = await fetch(response.url);

    if (!response.ok) return false;

    let data = await response.json();

    orders.orders = [
      ...orders.orders.filter((order) => order.id != data.order.id),
      { id: data.order.id, paid: data.order.paid },
    ];
    currentOrderId = data.order.id;

    return true;
  } catch (err) {
    console.error(err);

    return false;
  }
}

/**
 * Send the personal information to the API to complete the current order
 * @param {FormData} data
 * @returns {Promise<boolean>} false if the request fails in any way
 */
async function putPersonalInformations(data) {
  try {
    if (currentOrderId === undefined) return false;

    if (
      !data.get("email") ||
      !data.get("address") ||
      !data.get("postal-code") ||
      !data.get("city") ||
      !data.get("province") ||
      !data.get("country")
    )
      return false;

    let response = await fetch(`${API_URL}/order/${currentOrderId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        order: {
          email: data.get("email"),
          shipping_information: {
            address: data.get("address"),
            postal_code: data.get("postal-code"),
            city: data.get("city"),
            province: data.get("province"),
            country: data.get("country"),
          },
        },
      }),
    });

    return response.ok;
  } catch (err) {
    console.error(err);

    return false;
  }
}

/**
 * Send the credit card data to the API to complete the current order
 * @param {FormData} data
 * @returns {Promise<boolean>} false if the request fails in any way
 */
async function putCreditCard(data) {
  try {
    if (currentOrderId === undefined) return false;

    if (
      !data.get("name") ||
      !data.get("number") ||
      !data.get("expiration-month") ||
      !data.get("expiration-year") ||
      !data.get("cvv")
    )
      return false;

    let response = await fetch(`${API_URL}/order/${currentOrderId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        credit_card: {
          name: data.get("name"),
          number: data.get("number"),
          expiration_month: data.get("expiration-month"),
          expiration_year: data.get("expiration-year"),
          cvv: data.get("cvv"),
        },
      }),
    });

    // Reload the order after 2 seconds (paid badge)
    let orderId = currentOrderId;
    setTimeout(() => {
      getOrder(orderId);
    }, 2000);

    return response.ok;
  } catch (err) {
    console.error(err);

    return false;
  }
}

/**
 * @returns {Promise<Order>}
 */
async function getOrder(orderId) {
  let response = await fetch(`${API_URL}/order/${orderId}`);

  let data = await response.json();

  orders.orders = [
    ...orders.orders.filter((order) => order.id != data.order.id),
    { id: data.order.id, paid: data.order.paid },
  ];

  return data.order;
}

// === Cart ===

/**
 * @type {Observable<Cart>}
 */
let cart = makeObservable({ items: [] });

/**
 * @param {number} productId
 * @returns {void}
 */
function addToCart(productId) {
  let existingItem = cart.items.find((item) => item.id === productId);

  if (existingItem == undefined) {
    cart.items = [...cart.items, { id: productId, count: 1 }];
  } else {
    cart.items = [
      ...cart.items.filter((item) => item.id != existingItem.id),
      { id: existingItem.id, count: existingItem.count + 1 },
    ];
  }
}

/**
 * @param {number} productId
 * @returns {void}
 */
function removeFromCart(productId) {
  let item = cart.items.find((item) => item.id === productId);
  if (!item) return;

  if (item.count <= 1) {
    cart.items = [...cart.items.filter((cartItem) => cartItem.id != item.id)];
  } else {
    cart.items = [
      ...cart.items.filter((cartItem) => cartItem.id != item.id),
      { id: item.id, count: item.count - 1 },
    ];
  }
}

// === Observable ===

/**
 * @template T
 * @param {T} target
 * @returns {Observable<T>}
 */
function makeObservable(target) {
  let observers = Symbol("observers");

  target[observers] = [];

  target.observe = (observer) => {
    target[observers].push(observer);
  };

  return new Proxy(target, {
    set(target, property, value, _receiver) {
      let success = Reflect.set(...arguments);
      if (success) {
        target[observers].forEach((observer) => observer(property, value));
      }
      return success;
    },
  });
}

// == Types ===

/**
 * One of the products sent by the API
 * @typedef {{
 *   id: number
 *   name: string
 *   description: string
 *   price: number
 *   in_stock: boolean
 * }} Product
 */

/**
 * The products sentg by the API
 * @typedef {{
 *   products: Product[]
 * }} Products
 */

/**
 * @typedef {{
 *  id: number
 *  quantity: number
 * }} OrderProduct
 */

/**
 * The order sent by the API
 * @typedef {{
 *  id: number
 *  email: string
 *  paid: boolean
 *  total_price: number
 *  shipping_price: number
 *  products: OrderProduct[]
 *  shipping_information: {
 *   address: string
 *   postal_code: string
 *   city: string
 *   province: string
 *   country: string
 *  }
 *  credit_card: {
 *   name: string
 *   first_digits: string
 *   last_digits: string
 *   expiration_year: number
 *   expiration_month: number
 *  }
 *  transaction: {
 *    amount_charged: number
 *  } & {
 *    success: true
 *    id: string
 *  } | {
 *    success: false
 *    error: {
 *     code: string
 *     name: string
 *    }
 *  }
 * }} Order
 */

/**
 * Informations displayed in the order list
 * @typedef {{
 *  id: number
 *  paid: boolean
 * }} ShortOrder
 */

/**
 * An item of the cart
 * - `id` corresponds to a `Product`'s id
 * - `count` corresponds to the quantity of this product in the cart
 * @typedef {{
 *  id: number
 *  count: number
 * }} CartItem
 */

/**
 * The content of the cart
 * @typedef {{
 *  items: CartItem[]
 * }} Cart
 */

/**
 * Function called on update by an observable
 * @callback Observer
 * @param {string} property
 * @param {any} value
 * @returns {void}
 */

/**
 * Function to add an observer to an observable
 * @callback Observe
 * @param {Observer} observer
 * @returns {void}
 */

/**
 * @template T
 * @typedef {{
 *   observe: Observe
 * } & T} Observable<T>
 */
