class App {
    constructor() {
        this.stars(document.getElementById('stars'), window.innerWidth * 0.9)
        this.$text = document.querySelector('input[name="text"]')
        this.$translation = document.querySelector('.translation')
        document.querySelector('form').addEventListener('submit', e => this.translate(e))
    }

    stars(container, count) {
        for (let i = 0; i < count; i++) {
            let star = document.createElement('span')
            star.className = 'star ' + (i % 30 == 0 ? 'star-lg' : i % 15 == 0 ? 'star-md' : 'star')
            star.setAttribute(
                'style',
                `top: ${Math.round(Math.random() * window.innerHeight)}px; left: ${Math.floor(
                    Math.random() * window.innerWidth
                )}px`
            )
            container.appendChild(star)
        }
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
