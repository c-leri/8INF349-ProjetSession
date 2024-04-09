/**
 * @typedef {{
 *   id: number
 *   name: string
 *   description: string
 *   price: number
 *   in_stock: boolean
 * }} Product
 */

/**
 * @typedef {{
 *   products: Product[]
 * }} Products
 */

const API_URL = "http://localhost:5000/";

/**
 * @returns {Promise<Products>}
 */
async function fetch_products() {
  let response = await fetch(API_URL).catch((err) => console.error(err));

  return await response.json().catch((err) => console.error(err));
}
