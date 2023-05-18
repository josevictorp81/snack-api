const closeButton = document.querySelector('.close')
const messages = document.querySelector('.messages')

closeButton.addEventListener('click', () => {
    messages.style.display = 'none'
})
