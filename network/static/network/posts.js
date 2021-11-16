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
    // Select all the like buttons

    const editButtons = document.getElementsByClassName('edit-post-button')//Selected all the buttons
    const editPostForm = document.getElementsByClassName('edit-post-form')//Select all the forms
    const all_post_id = document.getElementsByClassName('post-id-edit')
    const all_edit_post_view = document.getElementsByClassName('edit-post-view')
    console.log(all_post_id)


    for (let i = 0; i < editButtons.length; i++) { // loop through each one and add an eventlistener
        editButtons[i].onclick = function () {
            // When edit button is clicked,the content of the post should be replaced with a textarea where its prepopulated with the existing post
            const thisEditPostForm = editPostForm[i]
            console.log(thisEditPostForm)
            console.log(i)

            // Create a textarea with prepolutated text
            const existingPost = document.createElement('textarea')
            existingPost.setAttribute('id', 'edit-post')
            existingPost.innerText = editButtons[i].parentElement.querySelector('#post-content').innerText

            // Create a submit button 
            const submitEditing = document.createElement('button')
            submitEditing.setAttribute('type', 'submit')
            submitEditing.setAttribute('class', 'btn btn-success')
            submitEditing.setAttribute('id', 'edit-post-buttom')
            submitEditing.innerText = "Save"

            // Append elements to the div
            thisEditPostForm.appendChild(existingPost)
            thisEditPostForm.appendChild(submitEditing)

            console.log(thisEditPostForm)

            all_edit_post_view[i].appendChild(thisEditPostForm)

            console.log(all_edit_post_view[i])
            all_edit_post_view[i].style.display = 'block'

            // Hide the edit button and its parent element
            editButtons[i].parentElement.style.display = 'none'
            console.log(all_post_id[i].innerText)

            thisEditPostForm.addEventListener('submit', (event) => {
                // stop form submission
                event.preventDefault()
                // call the send_post
                edit_post(all_post_id[i].innerText)

            })
            // Refresh the page 

        }

    }
    // make api request to edit the post
    function edit_post(post_id) {
        // Add the csrftoken to the header
        const request = new Request(
            'editpost/',
            { headers: { 'X-CSRFToken': csrftoken } }
        )
        console.log(request)
        // Make a POST request, passing in values for content
        fetch(request, {
            method: 'PUT',
            mode: 'same-origin',
            body: JSON.stringify({
                post_id: post_id,
                content: document.querySelector('#edit-post').value
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                // If successful, refresh the page with the lastest post
                // and empty the post form
                if (result.ok) {
                    location.reload()
                }
                else {
                    document.querySelector('#error-messages').innerText = result.error
                }
            })
    }










})