document.addEventListener('DOMContentLoaded', function () {
    // Select all the like buttons

    const allLikeUnlike = document.getElementsByClassName('like-unlike')
    const allPostIds = document.getElementsByClassName('post-id-like')

    const likesAmount = document.getElementsByClassName('likes-amount')

    for (let i = 0; i < allLikeUnlike.length; i++) {
        // if the current user is liking the post, set the heart color to black
        isLiking(allPostIds[i].innerText)

        allLikeUnlike[i].onclick = function () {


            if (allLikeUnlike[i].style.color === "black") {
                // means isLiking, click it will unlike the post
                likeUnlike(allPostIds[i].innerText, "unlike")// unlike the post
                allLikeUnlike[i].style.color = "Red" // change the color to red
                if (parseInt(likesAmount[i].innerText) > 0) {
                    likesAmount[i].innerText = parseInt(likesAmount[i].innerText) - 1
                } // reduce the like amount
            } else {
                likeUnlike(allPostIds[i].innerText, "like")// like the post
                allLikeUnlike[i].style.color = "Black" // change the color to red
                likesAmount[i].innerText = parseInt(likesAmount[i].innerText) + 1
                //increate the like amount

            }
        }
        function isLiking(postId) {
            fetch(`is_liking/${postId}`, {
                method: 'GET'

            })
                .then(response => response.json())
                .then(result => {
                    if (result.isLiking) {
                        allLikeUnlike[i].style.color = "Black"
                    } else {
                        allLikeUnlike[i].style.color = "Red"
                    }

                })


        }





    }

    // function isLiking(postId) {

    //     // Send a request to see if the current user is already liked the post
    //     fetch(`is_liking/${postId}`, {
    //         method: 'GET'

    //     })
    //         .then(response => response.json())
    //         .then(result => {
    //             return result.isLiking
    //         })
    // }
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
                console.log(result)
            })

    }







})