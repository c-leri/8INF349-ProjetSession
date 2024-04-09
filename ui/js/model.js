const API_URL = "http://localhost:5000/";

/**
 * @type {Observable<Products>}
 */
let products = makeObservable({ products: [] });

/**
 * @type {Observable<Cart>}
 */
let cart = makeObservable({ items: [] });

/**
 * Loads the products from the API into `products`
 * @returns {void}
 */
function loadProducts() {
  fetch(API_URL)
    .then((response) => {
      response.json().then((data) => {
        products.products = data.products;
      });
    })
    .catch((err) => console.error(err));
}

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
