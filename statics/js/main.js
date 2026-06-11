const hamburger = document.querySelector('.hamburger');
const nav = document.querySelector('header nav');

// باز و بسته کردن منوی همبرگری در موبایل
hamburger.addEventListener('click', () => {
  nav.classList.toggle('open');
});

// فقط بستن منو هنگام کلیک روی لینک‌ها در موبایل (بخش active حذف شد)
document.querySelectorAll('header nav a').forEach(link => {
  link.addEventListener('click', function () {
    if(window.innerWidth <= 768) {
        nav.classList.remove('open');
    }
  });
});
