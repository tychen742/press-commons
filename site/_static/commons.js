// Show the guides to staff (every role except students). Press enforces
// access on the server; this only avoids links that bounce visitors away.
(async () => {
  const STAFF = new Set(["ta", "instructor", "editor", "author", "admin"]);
  try {
    const r = await fetch("/api/me", { credentials: "include", cache: "no-store" });
    if (!r.ok) return;
    const me = await r.json();
    if (me.authenticated && STAFF.has(me.user.role)) document.documentElement.classList.add("tp-staff");
  } catch (e) { /* keep the visitor view */ }
})();

// The wordmark links to ThinkPress; the symbol and book name link to the cover.
document.addEventListener('DOMContentLoaded', function () {
    const style = document.createElement('style');
    style.textContent = '.tp-wordmark-link:focus-visible { outline: 2px solid #263e51; outline-offset: -2px; border-radius: 3px; }';
    document.head.appendChild(style);
    document.querySelectorAll('a.navbar-brand.logo').forEach(function (brand) {
        const holder = brand.parentElement;
        if (!holder || holder.querySelector('.tp-wordmark-link')) return;
        holder.style.position = 'relative';
        const press = document.createElement('a');
        press.className = 'tp-wordmark-link';
        press.href = 'https://thinkpress.org/';
        press.setAttribute('aria-label', 'ThinkPress');
        press.title = 'ThinkPress';
        press.style.position = 'absolute';
        press.style.zIndex = '2';
        holder.appendChild(press);
        function place() {
            const image = Array.from(brand.querySelectorAll('img')).find(img => img.offsetWidth > 0);
            if (!image) { press.style.display = 'none'; return; }
            press.style.display = 'block';
            const box = image.getBoundingClientRect();
            const origin = holder.getBoundingClientRect();
            press.style.left = `${box.left - origin.left + box.width * 74 / 280}px`;
            press.style.top = `${box.top - origin.top + box.height * 8 / 72}px`;
            press.style.width = `${box.width * 198 / 280}px`;
            press.style.height = `${box.height * 28 / 72}px`;
        }
        const watcher = new ResizeObserver(place);
        brand.querySelectorAll('img').forEach(function (img) {
            watcher.observe(img);
            img.addEventListener('load', place);
        });
        watcher.observe(holder);
        new MutationObserver(place).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
        window.addEventListener('resize', place);
        place();
    });
});
