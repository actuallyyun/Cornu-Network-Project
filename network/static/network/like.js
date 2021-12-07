document.addEventListener('DOMContentLoaded', function () {
    // Select all the like icons and store them in an array
    let LikeUnlikeIcons = Array.from(document.getElementsByClassName('like-unlike'))

    LikeUnlikeIcons.forEach(icon => {
        //First decide on the status of the liking and show the color accordingly
        isLiking(icon.dataset.postId).then(result => {
            if (result.isLiking) {
                //Update liking status
                icon.style.color = "Black"
                icon.addEventListener('click', (event) => {
                    console.log(event.target.parentElement.querySelector('.likes-amount'))
                    likeUnlike(event.target.dataset.postId, "unlike")
                    //Update the likes amount
                    likes = event.target.parentElement.querySelector('.likes-amount').innerText
                    event.target.parentElement.querySelector('.likes-amount').innerText = parseInt(likes) - 1
                    icon.style.color = "Red"
                })
            } else {
                icon.style.color = "Red"
                icon.addEventListener('click', (event) => {
                    console.log(event.target.parentElement.querySelector('.likes-amount'))
                    likeUnlike(event.target.dataset.postId, "like")
                    //Update the likes amount
                    likes = event.target.parentElement.querySelector('.likes-amount').innerText
                    event.target.parentElement.querySelector('.likes-amount').innerText = parseInt(likes) + 1
                    icon.style.color = "Black"
                })

            }
        })

    })
})