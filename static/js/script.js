fetch('header.html')
  .then(response => {
    if (response.ok) {
      return response.text();
    } else {
      throw new Error('Error: ' + response.status);
    }
  })
  .then(data => {
    const headerElement = document.createElement('div');
    headerElement.innerHTML = data;
    document.body.insertBefore(headerElement, document.body.firstChild);
  })
  .catch(error => {
    console.error(error);
  });