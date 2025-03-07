### 文件说明：Tokio 的 TcpSocket 实现

#### 文件目的
`tcp/socket.rs` 是 Tokio 网络模块中的核心文件，实现了 `TcpSocket` 结构体。该结构体用于在创建 `TcpStream` 或 `TcpListener` 之前，对 TCP 套接字进行细粒度配置。通过直接操作底层套接字选项（如 `SO_REUSEADDR`、`TCP_NODELAY` 等），开发者可以满足特定网络场景的需求。

---

#### 核心组件与功能

##### 1. **TcpSocket 结构体**
- **底层实现**：基于 `socket2` crate 封装的跨平台套接字接口，通过 `socket2::Socket` 管理操作系统级套接字。
- **主要用途**：
  - 配置套接字选项（如保持活动、缓冲区大小、非阻塞模式）。
  - 显式绑定地址或监听端口。
  - 转换为 `TcpStream` 或 `TcpListener`。

##### 2. **关键方法**
- **创建套接字**：
  - `new_v4()` / `new_v6()`：创建 IPv4 或 IPv6 的 TCP 套接字。
  - `new(domain)`：内部方法，设置非阻塞模式并初始化套接字。

- **配置选项**：
  - `set_keepalive`：启用/禁用 TCP 保活机制。
  - `set_reuseaddr`：允许绑定已使用的地址（跨平台支持）。
  - `set_nodelay`：禁用 Nagle 算法（即时发送数据包）。
  - `set_send_buffer_size` / `set_recv_buffer_size`：调整发送/接收缓冲区大小。

- **绑定与连接**：
  - `bind(addr)`：绑定到指定地址。
  - `listen(backlog)`：将套接字转换为监听器，设置最大连接队列长度。
  - `connect(addr)`：异步建立 TCP 连接，返回 `TcpStream`。

- **平台适配**：
  - 通过 `cfg` 宏处理 Unix/Windows 差异（如文件描述符 `RawFd` 或套接字句柄 `RawSocket`）。
  - 实现 `AsRawFd`/`AsRawSocket` 等 trait，提供对底层资源的访问。

##### 3. **高级功能**
- **从标准库套接字转换**：
  - `from_std_stream`：将 `std::net::TcpStream` 转换为 Tokio 的 `TcpSocket`，需确保非阻塞模式。
- **错误处理**：
  - `take_error()`：获取套接字的错误状态（如连接失败）。

---

#### 与其他组件的交互
- **与 TcpStream/TcpListener 的关系**：
  - `TcpSocket` 是中间配置层，最终通过 `connect` 或 `listen` 转换为 Tokio 的流或监听器。
  - 示例：
    ```rust
    let socket = TcpSocket::new_v4()?;
    let listener = socket.bind(addr)?.listen(1024)?;
    ```
- **依赖 `socket2` crate**：
  - 提供跨平台的套接字选项配置能力，如 `SO_REUSEPORT`（仅 Unix）。

---

#### 项目中的角色
该文件是 Tokio 网络栈的核心组件，为高级用户提供对 TCP 套接字的精细控制能力，支持定制化网络配置，确保 Tokio 在高性能或特殊场景下的灵活性与兼容性。
