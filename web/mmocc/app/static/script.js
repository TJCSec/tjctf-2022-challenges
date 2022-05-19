const POLL_INTERVAL = 5000;
const UPDATE_INTERVAL = 100;
const SPEED = 10;

const poll = async () => {
  const response = await fetch('/clicks');
  const { clicks, flag } = await response.json();
  if (typeof flag !== 'undefined') {
    document.querySelector('p').innerText = flag;
    return Infinity;
  }
  return clicks;
};

(async () => {
  const clicks = poll();
  let real = await clicks;
  let display = real;

  const span = document.querySelector('span');
  span.innerText = display;

  const button = document.querySelector('button');
  button.addEventListener('click', () => {
    display++;
    span.innerText = display;
    fetch('/click');
  });

  const updater = setInterval(() => {
    if (real === Infinity) {
      clearInterval(updater);
      display = real;
      span.innerText = display;
      return;
    }
    const diff = real - display;
    if (diff <= 0) return;
    const delta = Math.round(Math.min(diff / 2, Math.max(1, SPEED * UPDATE_INTERVAL * diff / POLL_INTERVAL)));
    display += delta;
    span.innerText = display;
  }, UPDATE_INTERVAL);

  const interval = setInterval(async () => {
    real = await poll();
    if (real === Infinity) {
      clearInterval(interval);
    }
  }, POLL_INTERVAL);
})();
