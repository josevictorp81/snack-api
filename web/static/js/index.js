// close messages

function closeMessagesAuto() {
    console.log('saiu')
    setTimeout(() => {
        document.querySelector('.messages').style.display = 'none'
        console.log('saiu 2')
    }, 3000)
}

function closeMessages() {
    document.querySelector('.messages').style.display = 'none'
}

// close delete modal
function deleteModal(state) {
    if (state === 'open') {
        document.querySelector('.box').style.display = 'block'
    } else {
        document.querySelector('.box').style.display = 'none'
    }
}
