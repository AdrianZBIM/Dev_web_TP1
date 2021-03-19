// The URL to fetch users from:
let url = new URL('http://bim.kaliko.me/api/users/');

// Gets the DOM element with ID "updateButton"
fetchBtn =  document.getElementById('updateButton');
// Hook the call to "load_json_resource" to this element onclick event
fetchBtn.onclick = () => { load_json_resource(url, populate, error_mgmt) };

// FUNCTIONS DEFINITION STARTS
/******************************/

/* LOAD_JSON_RESOURCE
 * url          : the url to fetch the resource from
 * handle_json  : the function to call to handle the response
 * handle_error : the function to call to handle error
 */
function load_json_resource (url, handle_json, handle_error) {
  // Set headers to inform the serveur we want JSON
  headers = { 'Accept': 'application/json', };
  fetch(url, { method: 'GET', headers: headers, mode: 'cors'})
    // Deal with the response as soon as it's received
    .then(response => {
      if (!response.ok) { // HTTP Errors
        throw new Error(response.status+': '+response.statusText);
      }
      // Get content-type header to ensure we actually got JSON
      const contentType = response.headers.get('content-type');
      if ( !contentType || !contentType.includes('application/json') ) {
        throw new TypeError("Oops, we haven't got JSON!");
      }
      // Send JSON to the next promise
      return response.json();
    })
    .then(data => { // Deal with the data as JSON here
      console.log(data);
      handle_json(data);
    })
    .catch(error =>{ // Intercepts errors
      handle_error(error);
    });
}

/* POPULATE
 * This function handles the json resource fetch by "load_json_resource".
 * It is called when the HTTP request on the JSON resource is resolved (cf.
 * call of "load_json_resource")
 *
 * The resource is exposed in "reponse" argument
 */
function populate (response) {
  // Response is an Array: https://javascript.info/array

  // Here is a log of the response, use browser dev tools to inspect the object
  console.log(response);

  // 1. Loop over element of response to populate a user list
  // You can use the "for..of" loop form to do so.
  // cf: https://javascript.info/array#loops
  
  for (let element of response)
  {
  	let ajout_list = document.createElement('li');
	ajout_list.innerHTML = element;
	usersList.append(ajout_list);
  }
  

  // WHITHIN THE FOR LOOP
    // Add some code to build users list
    // Have a look at this tutorial
    // https://javascript.info/modifying-document#insertion-methods
  // END FOR LOOP

  // 2. Add an info about number of users we got from the API (response lenght)
}

/* ERROR_MGMT
 * This function handes error trying to fetch the JSON resource
 * It is called when the HTTP request throw an exception (cf. call of
 * "load_json_resource")
 */
function error_mgmt(error) {
  // Print fetch error somewhere on the page
  document.getElementById('fetchError').innerHTML = error;
}
// FUNCTIONS DEFINITION ENDS
