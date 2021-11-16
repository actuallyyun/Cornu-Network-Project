
// This script deals with the follow/unfollow action, as well as updating the followers and following numbers

document.addEventListener('DOMContentLoaded', function () {

    const followButton = document.getElementById('follow-unfollow')
    const currentUser = document.getElementById('current-username').innerText.trim()
    const posterUser = document.getElementById('poster-username').innerText.trim()
    const posterId = document.getElementById('poster-id').innerText
    const followersButton = document.getElementById('followers-num')

    // If the user is looking at her own page, hide the button
    if (currentUser === posterUser) {
        followButton.style.display = 'none'
    } else {
        // Check if the user is already following by calling the isFollowing() function
        isFollwing(posterId)

        // When Follow button is clicked, send a request to the server. 
        followButton.onclick = function () {
            // If the text is follow, let the use follows
            if (followButton.textContent === "Follow") {
                manageFollowing(posterId, 'follow')
                followButton.textContent = "Unfollow"
                followButton.style.backgroundColor = "Red"
                // Increase this users' followers number
                followersButton.innerText = parseInt(followersButton.innerText) + 1
            } else {
                manageFollowing(posterId, 'unfollow')
                followButton.textContent = "Follow"
                followButton.style.backgroundColor = "Blue"
                // Reduce this users' followers number
                if (parseInt(followersButton.innerText) > 0) {
                    followersButton.innerText = parseInt(followersButton.innerText) - 1

                }
            }
        }
    }

    function manageFollowing(posterId, change) {

        // Send an AJAX request to achieve follow/unfollow function

        fetch(`/follow_user/${posterId}/${change}`, {
            method: 'PUT',
        })
            .then(response => response.json())
            .then(result => {
                //TODO in this case, what should be done with the result? For instance, should it provide feedback saying follow/unfollow successfully, 
                //as well as display error msg if not successfil.
                console.log(result)
            })

    }
    function isFollwing(posterId) {
        // Send a AJAX request to check if the current user is already following the poster
        fetch(`${posterId}/is_following/`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
                console.log(result.isFollowing)
                // Change the follow/unfollow button accordingly
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