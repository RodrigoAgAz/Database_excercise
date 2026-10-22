document.getElementById("shuffle-btn").addEventListener("click", () => {
    const list = document.getElementById("name-list");
    const items = Array.from(list.children);

    for (let i = items.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [items[i], items[j]] = [items[j], items[i]];
    }

    items.forEach((item) => list.appendChild(item));
});
