import assignments from "./assets/kart-assignments.json";

export default class Kart {
  constructor(id, x, y, ranking = 0) {
    this.id = id;
    this.x = x;
    this.y = y;
    this.ranking = ranking;
    // this.current_item = current_item;
  }

  get_name() {
    return assignments[this.id] || "Unknown";
  }

  get_title() {
    // removes the hypens and capitalizes the first letter of each word
    return this.get_name()
      .replace(/-/g, " ")
      .replace(/\b\w/g, (l) => l.toUpperCase());
  }

  static get_self_kart_id() {
    return assignments["my_id"];
  }
}
