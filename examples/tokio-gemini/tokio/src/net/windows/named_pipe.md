这个文件 `named_pipe.rs` 实现了 Tokio 对 Windows 命名管道的支持。它提供了 `NamedPipeServer` 和 `NamedPipeClient` 结构体，分别用于创建和管理命名管道的服务器端和客户端。

**主要组成部分：**

1.  **模块引用和依赖：**
    *   引入了标准库中的 `std::ffi`、`std::io`、`std::pin` 和 `std::task` 模块，用于处理 FFI、I/O 操作、Pinning 和异步任务。
    *   引入了 `crate::io`、`crate::os::windows::io` 模块，用于 Tokio 的 I/O 抽象和 Windows 相关的 I/O 操作。
    *   使用了 `cfg_io_util!` 宏，根据配置条件引入 `bytes::BufMut`，用于处理字节缓冲区。
    *   定义了 `doc` 模块，用于在文档生成时隐藏未使用的导入。

2.  **`NamedPipeServer` 结构体：**
    *   表示一个 Windows 命名管道服务器。
    *   包含一个 `io` 字段，类型为 `PollEvented<mio_windows::NamedPipe>`，用于异步 I/O 操作。
    *   提供了以下方法：
        *   `from_raw_handle`：从原始句柄创建服务器。
        *   `info`：检索关于命名管道的信息。
        *   `connect`：等待客户端连接。
        *   `disconnect`：断开服务器端的连接。
        *   `ready`：等待指定的就绪状态。
        *   `readable`：等待管道可读。
        *   `poll_read_ready`：轮询管道是否可读。
        *   `try_read`：尝试从管道读取数据。
        *   `try_read_vectored`：尝试从管道读取数据到多个缓冲区。
        *   `try_read_buf`：尝试从管道读取数据到 `BufMut` 缓冲区。
        *   `writable`：等待管道可写。
        *   `poll_write_ready`：轮询管道是否可写。
        *   `try_write`：尝试向管道写入数据。
        *   `try_write_vectored`：尝试向管道写入多个缓冲区的数据。
        *   `try_io`：使用用户提供的 I/O 操作。
        *   `async_io`：使用用户提供的异步 I/O 操作。
    *   实现了 `AsyncRead` 和 `AsyncWrite` trait，使得 `NamedPipeServer` 可以用于异步读写操作。
    *   实现了 `AsRawHandle` 和 `AsHandle` trait，用于获取原始句柄。

3.  **`NamedPipeClient` 结构体：**
    *   表示一个 Windows 命名管道客户端。
    *   包含一个 `io` 字段，类型为 `PollEvented<mio_windows::NamedPipe>`，用于异步 I/O 操作。
    *   提供了与 `NamedPipeServer` 类似的方法，用于客户端的 I/O 操作。
    *   实现了 `AsyncRead` 和 `AsyncWrite` trait，使得 `NamedPipeClient` 可以用于异步读写操作。
    *   实现了 `AsRawHandle` 和 `AsHandle` trait，用于获取原始句柄。

4.  **`ServerOptions` 结构体：**
    *   用于构建命名管道服务器的配置选项。
    *   提供了各种配置方法，如 `pipe_mode`、`access_inbound`、`access_outbound`、`first_pipe_instance`、`max_instances` 等。
    *   `create` 方法用于创建命名管道服务器。

5.  **`ClientOptions` 结构体：**
    *   用于构建命名管道客户端的配置选项。
    *   提供了各种配置方法，如 `read`、`write`、`security_qos_flags`、`pipe_mode` 等。
    *   `open` 方法用于打开命名管道客户端。

6.  **`PipeMode` 枚举：**
    *   定义了命名管道的模式，包括 `Byte` 和 `Message`。

7.  **`PipeEnd` 枚举：**
    *   定义了命名管道的端点，包括 `Client` 和 `Server`。

8.  **`PipeInfo` 结构体：**
    *   包含命名管道的信息，如模式、端点、最大实例数等。

9.  **辅助函数：**
    *   `encode_addr`：将字符串地址编码为宽字符串。
    *   `named_pipe_info`：从原始句柄获取命名管道信息。

**功能和作用：**

*   该文件提供了在 Tokio 运行时中使用 Windows 命名管道的 API。
*   它允许创建服务器端和客户端，并进行异步读写操作。
*   它提供了配置选项，用于控制命名管道的各种属性，如模式、访问权限等。
*   它处理了 Windows 命名管道相关的底层细节，如句柄管理、异步 I/O 等。
