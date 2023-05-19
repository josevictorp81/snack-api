const closeButton = document.querySelector('.close')
const messages = document.querySelector('.messages')

closeButton.addEventListener('click', () => {
    messages.style.display = 'none'
})

const inputModal = document.querySelector('.delete-input')
const closeModal = document.querySelector('.cancel-delete')
const modal = document.querySelector('.modal')

closeModal.addEventListener('click', () => {
    modal.style.display = 'none'
    inputModal.checked = false
})
