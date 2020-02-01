function show_errors(errors) {

    const Toast = Swal.mixin({
        toast: true,
        position: 'bottom',
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: true,
        onOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });

    let error_text = '';
    Array.from(Object.values(errors)).forEach(error => {
        error_text += error;
        error_text += '\n';
    });

    if (error_text !== '') {
        Toast.fire({
            icon: 'error',
            title: error_text,
        });
    }
}


function show_alerts(alerts) {

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        onOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    });

    let alert_text = '';
    Array.from(Object.values(alerts)).forEach(alert => {
        alert_text += alert;
        alert_text += '\n';
    });

    console.log(alert_text);
    if (alert_text !== '') {
        Toast.fire({
            icon: 'success',
            title: alert_text,
        });
    }


}