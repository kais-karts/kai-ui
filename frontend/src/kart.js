import assignments from "./assets/kart-assignments.json";

export default class Kart {
  constructor(id, x, y, current_item) {
    this.id = id;
    this.x = x;
    this.y = y;
    this.current_item = current_item;
  }

  get_name() {
    return assignments[this.id] || "Unknown";
  }
}
