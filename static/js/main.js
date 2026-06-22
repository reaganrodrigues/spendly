// main.js — students will add JavaScript here as features are built

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('videoModal');
    const modalTrigger = document.getElementById('videoModalTrigger');
    const modalClose = document.querySelector('.modal-close');
    const modalOverlay = document.querySelector('.modal-overlay');
    const videoFrame = document.getElementById('videoFrame');

    if (!modal || !modalTrigger) return;

    function openModal() {
        modal.classList.add('active');
    }

    function closeModal() {
        modal.classList.remove('active');
        stopVideo();
    }

    function stopVideo() {
        const src = videoFrame.src;
        videoFrame.src = src;
    }

    modalTrigger.addEventListener('click', openModal);
    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
});
