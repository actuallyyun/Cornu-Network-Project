document.addEventListener('DOMContentLoaded', function () {

    // The following scipt handles the make a new post function
    let postForm = document.querySelector('.post-form')
    postForm.addEventListener('submit', (event) => {
        // stop form from submission
        event.preventDefault()
        // call the send_post api
        send_post().then(result => {
            console.log(result)
            if (result.ok) {
                location.reload()
            } else {
                // TODO not sure what to do
            }
        })
    })


    // The following scipts deals with the edit post function
    // Select all the edit buttons and editForms
    let editBtns = Array.from(document.getElementsByClassName('edit-post-btn'))
    let editForms = Array.from(document.getElementsByClassName('edit-post-form'))

    // Iterate through all the edit buttons and add eventlistener to each one

    editBtns.forEach(editBtn => {
        editBtn.addEventListener('click', (event) => {
            console.log(event.target.parentElement)
            console.log(event.target.parentElement.parentElement)
            console.log(event.target.parentElement.parentElement.parentElement.querySelector('.edit-post-view'))

            // Display the edit-post-view and hide the display-view
            event.target.parentElement.style.display = 'none'
            event.target.parentElement.parentElement.parentElement.querySelector('.edit-post-view').style.display = 'block'

        })
    })

    // Iterate through the forms and add eventlistener too
    editForms.forEach(editForm => {
        editForm.addEventListener('submit', (e) => {
            // Stop form from submission
            e.preventDefault()
            // Call the edit post api and pass the form
            console.log(e.target)
            edit_post(e.target).then(result => {
                console.log(result)
                if (result.ok) {
                    location.reload()
                }
            })
        })
    })

})

