// close messages
function closeMessagesAuto() {
    setTimeout(() => {
        document.querySelector('.messages').style.display = 'none'
        document.querySelector('.messages').style.transition = '2s'
        document.querySelector('.messages').style.transitionProperty = 'display'
    }, 3000)
}

// close delete modal
function deleteModal(state) {
    if (state === 'open') {
        document.querySelector('.box').style.display = 'block'
    } else {
        document.querySelector('.box').style.display = 'none'
    }
}
