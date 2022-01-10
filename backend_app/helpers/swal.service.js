import Swal from "sweetalert2";

export const swalService = {
  showToast,
  showModal
};

function showToast(icon, message,_position="top-end") {
  const Toast = Swal.mixin({
    toast: true,
    position: _position,
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  Toast.fire({
    icon: icon,
    title: message
  })

}
function showModal(title, message,icon,_position="top-end") {
  Swal.fire({
    title:title,
    icon: icon,
    html: message,
    position: _position,
  })

}
