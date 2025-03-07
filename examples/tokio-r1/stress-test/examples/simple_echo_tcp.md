### Code Explanation: `simple_echo_tcp.rs`

#### Purpose
This file implements a **TCP echo server and client** to stress-test Tokio's asynchronous networking capabilities and detect memory leaks (via tools like Valgrind). It validates resource management under load by sending/receiving a high volume of data between server and client.

#### Key Components
1. **Constants**:
   - `TCP_ENDPOINT`: Server address (`127.0.0.1:8080`).
   - `NUM_MSGS`: Number of messages to send (100).
   - `MSG_SIZE`: Size of each message (1 KB).

2. **Server Setup**:
   - Runs in a dedicated Tokio runtime (`rt`).
   - Binds a `TcpListener`, accepts a connection, and splits the socket into read/write halves.
   - Uses `tokio::io::copy` to echo all received data back to the client indefinitely.

3. **Client Setup**:
   - Runs in a separate Tokio runtime (`rt2`).
   - Connects to the server, generates random 1 KB messages, and verifies echoed responses.
   - Sends a completion signal via a `oneshot` channel after all messages are processed.

4. **Synchronization**:
   - A `sleep` ensures the server binds before the client connects.
   - A `oneshot` channel blocks the main thread until the client completes all operations.

#### Project Role
This file acts as a **stress-testing tool** for Tokio's TCP stack. It ensures no memory/resource leaks occur under sustained load, validating the reliability of asynchronous I/O operations in the runtime. It complements other examples in the repository by focusing on long-running, high-throughput scenarios.
