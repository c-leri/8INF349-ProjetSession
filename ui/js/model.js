/**
 * The products received from the API
 * @typedef {{
 *   id: number
 *   name: string
 *   description: string
 *   price: number
 *   weight: number
 *   in_stock: boolean
 * }} Product
 */

/**
 * @param {Product} product
 * @returns {HTMLDivElement}
 */
function product_to_view(product) {
  let id = document.createElement("p");
  id.textContent = `Id: ${product.id}`;

  let name = document.createElement("p");
  name.textContent = `Name: ${product.name}`;

  let description = document.createElement("p");
  description.textContent = `Description: ${product.description}`;

  let price = document.createElement("p");
  price.textContent = `Price: ${product.price}`;

  let weight = document.createElement("p");
  weight.textContent = `Weight: ${product.weight}`;

  let in_stock = document.createElement("p");
  in_stock.textContent = `In Stock: ${product.in_stock}`;

  let root = document.createElement("div");
  root.append(id, name, description, price, weight, in_stock);

  return root;
}
