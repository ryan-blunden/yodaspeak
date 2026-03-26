class App {
  constructor() {
    this.form = document.querySelector("#translate-form");
    this.textInput = document.querySelector('input[name="text"]');
    this.translation = document.querySelector(".translation");
    this.stars = document.querySelector("#stars");

    App.renderStars(this.stars);
    this.form.addEventListener("submit", (event) => this.translate(event));
    window.addEventListener("resize", () => App.renderStars(this.stars));
  }

  static renderStars(container) {
    const count = Math.floor(window.innerWidth * 0.9);
    container.replaceChildren();

    for (let i = 0; i < count; i++) {
      const star = document.createElement("span");
      star.className =
        i % 30 === 0 ? "star star-lg" : i % 15 === 0 ? "star star-md" : "star";
      star.setAttribute(
        "style",
        `top: ${Math.round(
          Math.random() * window.innerHeight
        )}px; left: ${Math.floor(Math.random() * window.innerWidth)}px`
      );
      container.appendChild(star);
    }
  }

  translate(event) {
    event.preventDefault();
    this.translation.classList.add("hide");
    this.translation.classList.remove("show");

    const reveal = (translation) => {
      this.translation.innerText = `"${translation}"`;
      this.translation.classList.remove("hide");
      this.translation.classList.add("show");
    };

    fetch(this.form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: this.textInput.value }),
    })
      .then((res) => res.json())
      .then((data) => {
        reveal(data.translation || data.message);
      })
      .catch(() => {
        reveal("Sorry, am I, as translate your message, I cannot.");
      });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new App();
});
