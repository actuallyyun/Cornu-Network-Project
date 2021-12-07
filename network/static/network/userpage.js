
// This script deals with the follow/unfollow action in the userpage, as well as updating the followers and following numbers

document.addEventListener('DOMContentLoaded', function () {

    const followButton = document.getElementById('follow-unfollow')
    const currentUserId = document.querySelector('.nav-item').dataset.userId
    const posterId = document.querySelector('.display-post-view').dataset.posterId
    const followersNum = document.querySelector('.badge-followers-num')

    // If the user is looking at her own page, hide the button
    if (currentUserId === posterId) {
        followButton.style.display = 'none'
    } else {
        // Check if the user is already following by calling the isFollowing() function
        isFollwing(posterId).then(result => {
            console.log(result)
            console.log(result.isFollowing)
            if (result.isFollowing) {
                buttonStatus('following')
                // Add an eventlistener to the unfollow button to unfollow ths user
                followButton.addEventListener('click', (e) => {
                    manageFollowing(posterId, 'unfollow')
                    buttonStatus('notFollowing')
                })
            } else {
                buttonStatus('notFollowing')
                followButton.addEventListener('click', (e) => {
                    manageFollowing(posterId, 'follow')
                    buttonStatus('following')
                })
            }
        })
    }

    function buttonStatus(status) {
        if (status === 'following') {
            followButton.textContent = "Unfollow"
            followButton.style.backgroundColor = "Red"
            followersNum.innerText = parseInt(followersNum.innerText) + 1
        } else if (status === 'notFollowing') {
            followButton.textContent = "Follow"
            followButton.style.backgroundColor = "Blue"
            followersNum.innerText = parseInt(followersNum.innerText) - 1
        }
    }
})