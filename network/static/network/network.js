

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {

    // When Post button is clicked, call send_post function
    const form = document.getElementById('post-form')
    console.log(form)
    form.addEventListener('submit', (event) => {
        // stop form submission
        event.preventDefault()
        // call the send_post
        send_post()
    })


    function send_post() {
        // Add the csrftoken to the header
        const request = new Request(
            'makepost/',
            { headers: { 'X-CSRFToken': csrftoken } }
        )
        // Make a POST request to /post, passing in values for content
        fetch(request, {
            method: 'POST',
            mode: 'same-origin',
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
    function load_posts(group) {

        // Request the posts for a particular group
        fetch(`/getposts/${group}`)
            .then(response => response.json())
            .then(posts => {
                console.log(posts)
                // do something with the posts



            })

    }



})