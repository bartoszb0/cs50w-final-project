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
            mark_task(this);
            stats_change(this)
        })
    });

    function stats_change(element) {
        let tbd = document.querySelector('#stats_tbd')
        let finished = document.querySelector('#stats_finished')

        if (element.innerHTML === '☐') {
            tbd.innerHTML = parseInt(tbd.innerHTML) + 1;
            finished.innerHTML = parseInt(finished.innerHTML) - 1;
        } else if ((element.innerHTML === '▣')) { 
            tbd.innerHTML = parseInt(tbd.innerHTML) - 1;
            finished.innerHTML = parseInt(finished.innerHTML) + 1;
        }
    }



    function mark_task(element) {
        const id = element.parentElement.querySelector('.task_name').getAttribute('data-task-id');
        const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


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


    //Open and close modal for deleting user
    document.querySelectorAll('.delete_but').forEach(function(element) {
        element.addEventListener('click', function() {
            this.parentElement.querySelector('.myModal-container').classList.add('show');
        })
    })

    document.querySelectorAll('.confirm_delete').forEach(function(element) {
        element.addEventListener('click', function() {
            delete_user(element.getAttribute('content'))
        })
    })

    function delete_user(user_id) {
        const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        fetch('new_user', {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
                user_id: user_id,
            })
        })
        .then(response => {
            if (response.status === 204) {
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                console.log('Success:', data);
            } else {
                console.log('User deleted successfully.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        location.reload()
    }


    // Display UNFINISHED or FINISHED TASKS
    const finished_but = document.querySelector('#finished')
    const finished_tab = document.querySelector('#finished_div')

    const unfinished_tab = document.querySelector('#unfinished_div')
    const unfinished_but = document.querySelector('#unfinished')

    finished_tab.style.display = 'none';
    finished_but.classList.add('hidden');

    finished_but.addEventListener('click', function() {
        finished_but.classList.remove('hidden');
        unfinished_but.classList.add('hidden');
        unfinished_tab.style.display = 'none';
        finished_tab.style.display = 'block';
    });

    unfinished_but.addEventListener('click', function() {
        unfinished_but.classList.remove('hidden');
        finished_but.classList.add('hidden');
        finished_tab.style.display = 'none';
        unfinished_tab.style.display = 'block';
    })

})