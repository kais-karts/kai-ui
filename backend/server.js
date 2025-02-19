// const WebSocket = require("ws");
// const { SerialPort, ReadlineParser } = require("serialport");

// const wss = new WebSocket.Server({ port: 8080 }); // WebSocket Server
// // const port = new SerialPort({ path: "COM15", baudRate: 115200 }); // Change port if needed
// // const parser = port.pipe(new ReadlineParser({ delimiter: "\n" })); // Serial data parser

// // WebSocket connection
// wss.on("connection", (ws) => {
//   console.log("Client connected");

//   // parser.on("data", (line) => {
//   //   console.log(line);
//   //   const parts = line.trim().split(",");
//   //   if (parts.length === 4) {
//   //     const data = {
//   //       id: parseInt(parts[0], 10),
//   //       msg: parseInt(parts[1], 10),
//   //       x: parseInt(parts[2], 10),
//   //       y: parseInt(parts[3], 10),
//   //     };
//   //     ws.send(JSON.stringify(data)); // Send JSON over WebSocket
//   //   }
//   // });

//   ws.on("close", () => console.log("Client disconnected"));
// });

// console.log("WebSocket server running on ws://localhost:8080");
