
document.addEventListener('DOMContentLoaded', function () {

    // When Follow button is clicked, send a request to the server. 
    // TODO This button should have two texts, follow, and unfollow.

    const followButton = document.getElementById('follow-unfollow')
    const currentUser = document.getElementById('current-username').innerText
    const posterUser = document.getElementById('poster-username').innerText
    const posterId = document.getElementById('poster-id').innerText

    // If the user is looking at her own page, hide the button
    if (currentUser === posterUser) {
        followButton.style.visibility = 'hidden'
    } else {
        followButton.onclick = function () {
            // If the text is follow, let the use follows
            if (followButton.textContent === "Follow") {
                follow_user()

            } else {
                unfollow_user()
                // and set the text to "follow"
                followButton.textContent === "Follow"
            }
        }

    }



    function follow_user() {

        // Send an AJAX request with the target user info, get it from the DOM page
        // maybe user a PUT request?
        fetch('follow_user/', {
            method: 'PUT',
            body: JSON.stringify({
                following_user: posterUser
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                // and set the text to "unfollow"
                followButton.textContent = "Unfollow"
                followButton.style.backgroundColor = "Red"
            })

    }

    function unfollow_user() {

        // Send an AJAX request with the target user info, get it from the DOM page
        // maybe user a PUT request?
        fetch('unfollow_user/', {
            method: 'PUT',
            body: JSON.stringify({
                following_user: posterUser
            })
        })

    }


})