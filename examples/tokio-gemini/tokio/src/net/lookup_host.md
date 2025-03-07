这个文件定义了 `tokio::net` 模块中的 `lookup_host` 函数，用于执行 DNS 解析。

**主要组成部分：**

*   **`cfg_net!` 宏：**  这是一个条件编译宏，确保只有在启用了 `net` 特性时，才会编译该文件中的代码。
*   **`use` 语句：**  引入了必要的模块和类型，包括 `crate::net::addr` (用于地址转换), `std::io` (用于 I/O 操作), 和 `std::net::SocketAddr` (表示套接字地址)。
*   **`lookup_host` 函数：**
    *   **功能：**  执行 DNS 解析，将主机名或 IP 地址转换为一个或多个 `SocketAddr`。
    *   **参数：**  接受一个实现了 `ToSocketAddrs` trait 的类型 `T`，这意味着它可以是字符串（例如 "localhost:3000"）或其他可以转换为套接字地址的类型。
    *   **返回值：**  返回一个 `io::Result<impl Iterator<Item = SocketAddr>>`。  `io::Result` 表示操作可能失败，并返回一个 `io::Error`。  `impl Iterator<Item = SocketAddr>` 表示一个迭代器，它会产生零个或多个 `SocketAddr`，这些地址是 DNS 解析的结果。
    *   **实现：**  调用了 `addr::to_socket_addrs(host).await`，将 `host` 转换为套接字地址。  `await` 关键字表明这是一个异步操作，它会等待 DNS 解析完成。
*   **文档注释：**  提供了关于 `lookup_host` 函数的详细说明，包括其用途、用法示例和注意事项。  特别强调了该 API 并非为所有 DNS 用例设计，对于更复杂的场景，建议使用专门的 DNS 库。

**与其他文件的关系：**

*   **`addr` 模块：**  `lookup_host` 函数依赖于 `addr` 模块中的 `to_socket_addrs` 函数，该函数负责实际的地址转换和 DNS 解析。
*   **`ToSocketAddrs` trait：**  `lookup_host` 函数使用 `ToSocketAddrs` trait，该 trait 定义了将类型转换为套接字地址的接口。  `str` 类型实现了这个 trait，允许直接使用字符串作为主机名。
