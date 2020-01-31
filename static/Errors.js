function show_errors(errors) {

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

    let error_text = '';
    Array.from(Object.values(errors)).forEach(error => {
        error_text += error;
        error_text += '\n';
    });

    Toast.fire({
        icon: 'error',
        title: error_text,
    });

}