// Fetch and insert the header content
function insertHeader() {
  fetch('templateFiles/header.html')
    .then(response => {
      if (response.ok) {
        return response.text();
      } else {
        throw new Error('Error: ' + response.status);
      }
    })
    .then(data => {
      const headerElement = document.getElementById('header');
      headerElement.innerHTML = data;
    })
    .catch(error => {
      console.error(error);
    });
}

// Call the insertHeader function when the page loads
document.addEventListener('DOMContentLoaded', insertHeader);