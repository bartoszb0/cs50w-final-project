document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.checkbox').forEach(element => {
        handle_checkbox(element)
    });

    function handle_checkbox(element) {
        element.addEventListener('click', function() {
            if (this.innerHTML === '☐') {
                this.innerHTML = '▣'
                this.parentElement.style.color = 'grey';
                this.setAttribute("title", "Unnmark");
            } else {
                this.innerHTML = '☐'
                this.parentElement.style.color = '#dee2e6';
                this.setAttribute("title", "Mark as finished");
            }
            console.log(this.parentElement)
        });
    }

})