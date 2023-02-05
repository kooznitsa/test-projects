let sortForm = document.getElementById('sortForm')
let pageLinks = document.getElementsByClassName('page-link')

if (sortForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function(e) {
            e.preventDefault()
            let page = this.dataset.page
            sortForm.innerHTML += `<input value=${page} name="page" hidden />`;
            sortForm.submit();
        })
    }
}