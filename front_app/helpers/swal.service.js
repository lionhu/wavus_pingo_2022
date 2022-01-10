import Swal from "sweetalert2";

export const swalService = {
  showToast,
  showModal,
  showConfirmModal
};

function showToast(icon, message,_position="top-end",_timer=3000) {
  const Toast = Swal.mixin({
    toast: true,
    position: _position,
    showConfirmButton: false,
    timer: _timer,
    timerProgressBar: !!_timer,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  console.log(_timer)
  Toast.fire({
    icon: icon,
    title: message
  })

}
function showModal(title, message,icon) {
  Swal.fire({
    title:title,
    icon: icon,
    html: message
  })
}

async function showConfirmModal(icon,title,text,confirmText){
  Swal.fire({
  title: title,
  text: text,
  icon: icon,
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: confirmText
}).then((result) => {
  return !!result.isConfirmed
})
}
