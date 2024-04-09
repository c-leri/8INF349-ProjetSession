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

let unused = {};
