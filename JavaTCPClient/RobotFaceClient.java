import java.io.*;
import java.net.*;

public class RobotFaceClient {

    private static final String HOST = "localhost";
    private static final int DEFAULT_PORT = 30001;

    public static void main(String[] args) throws Exception {

        int port = args.length > 0 ? Integer.parseInt(args[0]) : DEFAULT_PORT;

        System.out.println("Connecting to Robot Face on " + HOST + ":" + port + "...");
        Socket socket = new Socket(HOST, port);
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));

        System.out.println("Connected! Type commands below:");
        System.out.println("  eye left | eye right | eye center | eye 0-90");
        System.out.println("  sound gs | sound on  | sound off  | sound g");
        System.out.println("  Type 'exit' to quit.");
        System.out.println("─".repeat(50));

        // ── Reader thread — prints anything Python sends back ──
        Thread readerThread = new Thread(() -> {
            try {
                String response;
                while ((response = in.readLine()) != null) {
                    System.out.println("← Python: " + response);
                }
            } catch (IOException e) {
                System.out.println("Reader disconnected.");
            }
        });
        readerThread.setDaemon(true);
        readerThread.start();

        // ── Main thread — sends user input to Python ──
        String line;
        while ((line = userInput.readLine()) != null) {
            if (line.equalsIgnoreCase("exit")) {
                break;
            }
            out.println(line);
            System.out.println("→ Sent: " + line);
        }

        socket.close();
        System.out.println("Disconnected.");
    }
}