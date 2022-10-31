jQuery(document).ready(function ($) {
    $('#sidebar-nav a').each(function () {
        let link = this.href
        if (location == link) {
            $(this).addClass('active')
            let navItem = $(this).closest('.nav-item')
            navItem.children('a.nav-link').removeClass('collapsed')
            navItem.children('ul.nav-content').removeClass('collapse')
            $(this).removeClass('collapsed')
        }
    })
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');