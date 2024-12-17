class App {
    constructor() {
        this.$text = document.querySelector('input[name="text"]')
        this.$translation = document.querySelector('.translation')
        document.querySelector('form').addEventListener('submit', e => this.translate(e))
    }

    translate(event) {
        event.preventDefault()
        this.$translation.classList.add('hide')
        this.$translation.classList.remove('show')

        const reveal = translation => {
            this.$translation.innerText = `"${translation}"`
            this.$translation.classList.remove('hide')
            this.$translation.classList.add('show')
        }

        fetch('/api/translate', {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: this.$text.value }),
        })
            .then(res => res.json())
            .then(data => {
                reveal(data.translation ? data.translation : data.message)
            })
            .catch(error => {
                reveal('Sorry, am I, as translate your message, I cannot.')
            })
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App()
})
