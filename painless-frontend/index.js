// Function to send HTTP request to the server
function sendHttpRequest(consumberid, state) {
    // Replace this URL with the URL of your backend server
    const url = `http://localhost:8080/send/${consumberid}/${state}`;
  
    // Use the Fetch API to send the HTTP request
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Optional: You can handle the response data here
    })
    .catch(error => {
      console.error("Error sending HTTP request:", error);
    });
  }
  
  // Add event listeners to the checkboxes
  document.getElementById("button1").addEventListener("change", function() {
    const state = this.checked ? 1 : 0;
    sendHttpRequest(1, state);
  });
  
  document.getElementById("button2").addEventListener("change", function() {
    const state = this.checked ? 1 : 0;
    sendHttpRequest(2, state);
  });
  
  document.getElementById("button3").addEventListener("change", function() {
    const state = this.checked ? 1 : 0;
    sendHttpRequest(3, state);
  });
  
  document.getElementById("button4").addEventListener("change", function() {
    const state = this.checked ? 1 : 0;
    sendHttpRequest(4, state);
  });
  