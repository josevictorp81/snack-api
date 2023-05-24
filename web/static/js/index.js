// close messages
const closeButton = document.querySelector('.close')
const messages = document.querySelector('.messages')

closeButton.addEventListener('click', () => {
    messages.style.display = 'none'
})

function deleteModal(state) {
    if (state === 'open') {
        document.querySelector('.modal-box').style.display = 'block'
        console.log('abriu')
    } else {
        document.querySelector('.modal-box').style.display = 'none'
        console.log('fechou')
    }
}
