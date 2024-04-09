fetch("http://localhost:5000")
  .then((response) => {
    response.json().then((data) => {
      document.body.append(
        ...data.products.map((product) => product_to_view(product))
      );
    });
  })
  .catch((err) => console.error(err));
