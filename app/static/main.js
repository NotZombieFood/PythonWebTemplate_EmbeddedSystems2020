function formFail(error_message) {
    iziToast.error({
        id: 'error',
        title: 'Error',
        message: error_message,
        position: 'topRight',
        transitionIn: 'fadeInDown',
        icon: 'fas fa-exclamation-triangle'
    });
}


