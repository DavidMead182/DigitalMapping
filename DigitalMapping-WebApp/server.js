import express from "express";
import http from "http";
import { Server } from "socket.io";
import { SerialPort, ReadlineParser } from "serialport";
import cors from "cors";

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
  },
});

app.use(cors());

const portName = "COM7"; // Change to your port (Linux: "/dev/ttyUSB0", Mac: "/dev/tty.usbserial-XXXXX")

const serialPort = new SerialPort({ path: portName, baudRate: 9600 });
const parser = serialPort.pipe(new ReadlineParser({ delimiter: "\n" }));

serialPort.on("open", () => {
  console.log("Serial Port Opened");
});

parser.on("data", (data) => {
  console.log("Data from Microcontroller:", data);
  io.emit("serialData", data); // Send data to frontend via WebSockets
});

io.on("connection", (socket) => {
  console.log("Frontend connected");
  socket.on("disconnect", () => {
    console.log("Frontend disconnected");
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
