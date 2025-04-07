document.addEventListener('DOMContentLoaded', function() {

    // Check if the task is after the deadline
    const date = new Date();
    const year = date.getFullYear();
    const day = date.getDate();
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const month = monthNames[date.getMonth()];
    const today = new Date(`${month} ${day}, ${year}`);

    document.querySelectorAll('.deadline').forEach(function(element) {
        const deadlineDate = new Date(element.innerHTML);
        if (deadlineDate < today) {
            element.style.color = 'grey';
        }
        else if (deadlineDate.getTime() === today.getTime()) {
            element.style.color = '#e36056';
        }
    })


    // Unmarking and marking task as done
    document.querySelectorAll('.checkbox').forEach(function(element) {
        element.addEventListener('click', function() {
            if (this.innerHTML === '☐') {
                this.innerHTML = '▣'
                this.parentElement.style.color = 'grey';
            } else if ((this.innerHTML === '▣')) {
                this.innerHTML = '☐'
                this.parentElement.style.color = '#dee2e6';          
            }
            mark_task(element);
        })
    });

    function mark_task(element) {
        const id = element.parentElement.querySelector('.task_name').getAttribute('data-task-id');
        const csrf_token = element.getAttribute('content')

        fetch('marktask', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
                task_id: id,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
    }


    // Change shown table (finished or unfinished)
    const finished_heading = document.querySelector('#finished')
    const unfinished_heading = document.querySelector('#unfinished')
    const finished_table = document.querySelector('#finished_table')
    const unfinished_table = document.querySelector('#unfinished_table')


    finished_table.style.display = 'none';
    finished_heading.classList.add('hidden')

    unfinished_heading.addEventListener('click', function() {
        finished_table.style.display = 'none';
        unfinished_table.style.display = 'block';
        this.classList.remove('hidden');
        finished_heading.classList.add('hidden');
    });

    finished_heading.addEventListener('click', function() {
        finished_table.style.display = 'block';
        unfinished_table.style.display = 'none';
        this.classList.remove('hidden');
        unfinished_heading.classList.add('hidden');
    });


    // Open and close modal for task
    document.querySelectorAll('.task_name').forEach(function(element) {
        element.addEventListener('click', function() {
            const id = element.getAttribute('data-task-id');
            document.getElementById('modal-' + id).classList.add('show');
        })
    });

    document.querySelectorAll('.close').forEach(function(element) {
        element.addEventListener('click', function() {
            element.closest('.myModal-container').classList.remove('show');
        })
    });


})