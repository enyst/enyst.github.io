document.querySelectorAll('button[data-time]').forEach(button => {
  button.addEventListener('click', () => {
    const film = document.getElementById(button.getAttribute('aria-controls'));
    if (!film) return;
    film.currentTime = Number(button.dataset.time);
    film.play().catch(() => film.focus());
  });
});
