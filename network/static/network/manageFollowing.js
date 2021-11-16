
document.addEventListener('DOMContentLoaded', function () {

    // When Follow button is clicked, send a request to the server. 

    const followButton = document.getElementById('follow-unfollow')
    const currentUser = document.getElementById('current-username').innerText.trim()
    const posterUser = document.getElementById('poster-username').innerText.trim()
    const posterId = document.getElementById('poster-id').innerText
    const followersButton = document.getElementById('followers-num')

    // If the user is looking at her own page, hide the button
    if (currentUser === posterUser) {
        followButton.style.display = 'none'
    } else {
        // Check if the user is already following
        isFollwing(posterId)

        followButton.onclick = function () {
            // If the text is follow, let the use follows
            if (followButton.textContent === "Follow") {
                manageFollowing(posterId, 'follow')
                followButton.textContent = "Unfollow"
                followButton.style.backgroundColor = "Red"
                // TODO Increase this users' followers number
                followersButton.innerText = parseInt(followersButton.innerText) + 1


            } else {
                manageFollowing(posterId, 'unfollow')
                followButton.textContent = "Follow"
                followButton.style.backgroundColor = "Blue"
                // TODO Reduce this users' followers number
                if (parseInt(followersButton.innerText) > 0) {
                    followersButton.innerText = parseInt(followersButton.innerText) - 1

                }
            }
        }
    }

    function manageFollowing(posterId, change) {

        // Send an AJAX request with the target user info, get it from the DOM page

        fetch(`/follow_user/${posterId}/${change}`, {
            method: 'PUT',
        })
            .then(response => response.json())
            .then(result => {
                console.log(result)
            })

    }
    function isFollwing(posterId) {
        // Send a request to see if the current user is already following the poster
        fetch(`${posterId}/is_following/`, {
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