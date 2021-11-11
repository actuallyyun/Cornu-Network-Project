
document.addEventListener('DOMContentLoaded', function () {

    // When Follow button is clicked, send a request to the server. 

    const followButton = document.getElementById('follow-unfollow')
    const currentUser = document.getElementById('current-username').innerText
    const posterUser = document.getElementById('poster-username').innerText
    const posterId = document.getElementById('poster-id').innerText

    // If the user is looking at her own page, hide the button
    if (currentUser === posterUser) {
        followButton.style.visibility = 'hidden'
    } else {
        // Check if the user is already following
        isFollwing()

        followButton.onclick = function () {
            // If the text is follow, let the use follows
            if (followButton.textContent === "Follow") {
                manageFollowing('follow')
                followButton.textContent = "Unfollow"
                followButton.style.backgroundColor = "Red"
            } else {
                manageFollowing('unfollow')
                followButton.textContent = "Follow"
                followButton.style.backgroundColor = "Blue"
            }
        }
    }

    function manageFollowing(change) {

        // Send an AJAX request with the target user info, get it from the DOM page
        // maybe user a PUT request?

        fetch(`follow_user/${change}`, {
            method: 'PUT',
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                // and set the text to "unfollow"
            })

    }
    function isFollwing() {
        // Send a request to see if the current user is already following the poster
        fetch('is_following/', {
            method: 'GET',
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                console.log(result.isFollowing)
                if (result.isFollowing) {
                    followButton.textContent = "Unfollow"
                    followButton.style.backgroundColor = "Red"
                } else {
                    followButton.textContent = "Follow"
                    followButton.style.backgroundColor = "Blue"
                }

            })
    }

})