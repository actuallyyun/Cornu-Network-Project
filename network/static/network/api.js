// This scipts deals with editing posts function.I t also decides when to or not to show the edit button.
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

// Make API request to make a new post
function send_post() {
    return fetch('makepost/', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#post-content').value
        })
    })
        .then(response => response.json())
}


// make api request to edit the post
function edit_post(editForm) {
    // Make a POST request, passing in values for content
    console.log(editForm['elements'][1].value)
    console.log(editForm.dataset.postId)
    return fetch('editpost/', {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            post_id: editForm.dataset.postId,
            content: editForm['elements'][1].value
        })
    })
        .then(response => response.json())

}


function likeUnlike(postID, action) {
    // send a put request to change the like and unlike status in the database
    fetch(`like_unlike/${action}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: postID
        })

    })
        .then(response => response.json())
        .then(result => {
        })

}


function isLiking(postId) {
    return fetch(`is_liking/${postId}`, {
        method: 'GET'
    })
        .then(response => response.json())
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
    return fetch(`${posterId}/is_following/`, {
        method: 'GET',
    })
        .then(response => response.json())

}