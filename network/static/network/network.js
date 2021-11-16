// This scipts manages the post form and deals with the post request

document.addEventListener('DOMContentLoaded', function () {

    // When Post button is clicked, call send_post function
    const form = document.getElementById('post-form')
    form.addEventListener('submit', (event) => {
        // stop form submission
        event.preventDefault()
        // call the send_post
        send_post()
    })


    function send_post() {
        // Make a POST request to /makepost, passing in values for content
        fetch('makepost/', {
            method: 'POST',
            body: JSON.stringify({
                content: document.querySelector('#post-content').value
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                // If successful, refresh the page with the lastest post
                // and empty the post form
                if (result.ok) {
                    location.reload()
                    document.querySelector('#post-content') = 'What is happening'
                }
                else {
                    document.querySelector('#error-messages').innerText = result.error
                }
            })
    }

})