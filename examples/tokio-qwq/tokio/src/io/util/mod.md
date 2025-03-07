# 文件说明：`tokio/src/io/util/mod.rs`

## **文件目的**  
该文件是 Tokio 异步 I/O 工具模块的入口文件，负责组织和导出与异步 I/O 操作相关的实用工具、扩展 trait 和核心结构体。它为 Tokio 提供了高效的缓冲读写、数据复制、流处理等能力，简化异步 I/O 操作的实现。

---

## **关键组件与功能**

### **1. 扩展 Trait**
- **`AsyncBufReadExt`**: 为 `AsyncBufRead` trait 提供扩展方法，支持按行读取、填充缓冲区等操作。
- **`AsyncReadExt`**: 为 `AsyncRead` trait 提供便捷方法（如 `read_to_end`、`read_exact`），简化异步读取操作。
- **`AsyncSeekExt`**: 扩展 `AsyncSeek` trait 的寻址功能。
- **`AsyncWriteExt`**: 为 `AsyncWrite` trait 提供便捷写入方法（如 `write_all`、`flush`）。

### **2. 核心结构体**
- **`BufReader`**: 异步缓冲读取器，减少磁盘/网络读取的系统调用次数。
- **`BufWriter`**: 异步缓冲写入器，批量写入数据以提高效率。
- **`BufStream`**: 结合读写缓冲的流结构，适用于需要同时读写的场景。
- **`Lines`**: 按行解析异步流的迭代器。
- **`Split`**: 将双向流（如 TCP 流）拆分为独立的读取和写入半流。
- **`Take`**: 限制流中可读/写的字节数。

### **3. 工具函数**
- **`copy`**: 异步复制数据从一个流到另一个流。
- **`copy_bidirectional`**: 双向流数据复制，适用于需要同时读写双方的场景。
- **`empty`/`repeat`/`sink`**: 提供空流、重复流和黑洞流（丢弃输入）的实现。
- **`duplex`/`simplex`**: 创建内存管道流，用于进程间通信。

### **4. 配置与平台适配**
- **`cfg_io_util!`**: 宏条件编译，包含主要 I/O 工具模块。
- **`cfg_coop!`/`cfg_not_coop!`**: 根据 Tokio 的协作调度配置，控制任务进度跟踪逻辑（如 `poll_proceed_and_make_progress`）。
- **`DEFAULT_BUF_SIZE`**: 默认缓冲区大小（8KB），与标准库 `BufReader`/`BufWriter` 一致。

---

## **与其他模块的关联**
- **`tokio::io`**: 该文件导出的 trait 和结构体是 Tokio 异步 I/O 核心功能的实现基础。
- **`tokio::net`**: 网络模块（如 TCP/UDP）依赖这些工具处理流式数据。
- **`tokio::process`**: 进程间通信（如管道）使用 `BufStream` 和 `DuplexStream`。

---

## **文件在项目中的角色**  