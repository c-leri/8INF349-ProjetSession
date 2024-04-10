const API_URL = "http://localhost:5000";

/**
 * @type {Observable<Products>}
 */
let products = makeObservable({ products: [] });

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

async function postOrder() {
  fetch(`${API_URL}/order`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      products: [
        ...cart.items.map((item) => ({ id: item.id, quantity: item.count })),
      ],
    }),
  })
    .then((response) => {
      if (!response.ok) return;

      cart.items = [];
    })
    .catch((err) => {
      console.error(err);
    });
}

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
 * The order sent by the API
 * @typedef {{
 *  id: number
 *  email: string
 *  paid: boolean
 *  total_price: number
 *  shipping_price: number
 *  products: {
 *   id: number
 *   quantity: number
 *  }[]
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
