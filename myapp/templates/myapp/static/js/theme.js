document.addEventListener('DOMContentLoaded', (event) => {
    const theme = getCookie('theme');
    if (theme) {
        document.getElementById('theme-link').href = `/static/css/` + theme + `.css`;
    }
});

function toggleTheme() {
    const currentTheme = document.getElementById('theme-link').getAttribute('href');
    let newTheme = 'light';
    if (currentTheme.includes('light')) {
        newTheme = 'dark';
    }
    document.getElementById('theme-link').href = `/static/css/` + newTheme + `.css`;
    setCookie('theme', newTheme, 365);
}

function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days*24*60*60*1000));
    const expires = `expires=${d.toUTCString()}`;
    document.cookie = `${name}=${value};${expires};path=/`;
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i=0; i<ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
