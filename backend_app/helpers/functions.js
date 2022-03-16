import { axios } from "@/plugins/axios.js";

export const Functions = {
  get_order_status_badge_color
};

function get_order_status_badge_color(order_status) {
  let _color = "success";
  switch (order_status.toLowerCase()) {
    case "new":
      _color = "danger";
      break;
    case "processing":
      _color = "warning";
      break;
    case "delivering":
      _color = "primary";
      break;
    case "completed":
      _color = "success";
      break;
    default:
      _color = "secondary";
  }
  return _color;
}
