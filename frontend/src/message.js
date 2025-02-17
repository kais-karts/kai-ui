export default class Message {
  constructor(id, x, y, msg) {
    this.id = id;
    this.msg = msg;
    this.x = x;
    this.y = y;
  }

  static fromString(line) {
    const parts = line.trim().split(",");
    if (parts.length === 4) {
      return new Message(
        parseInt(parts[0], 10),
        parseInt(parts[1], 10),
        parseInt(parts[2], 10),
        parseInt(parts[3], 10),
        ""
      );
    }
    return null;
  }
}
