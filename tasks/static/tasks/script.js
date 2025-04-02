document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.checkbox').forEach(element => {
        handle_checkbox(element)
    });

    function handle_checkbox(element) {
        element.addEventListener('click', function() {
            if (this.innerHTML === '☐') {
                this.innerHTML = '▣'
            } else {
                this.innerHTML = '☐'
            }
        });
    }

})