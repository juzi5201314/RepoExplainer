# Unix 域套接字辅助模块

## 功能概述  
该文件为 Tokio 的 Unix 域套接字（Unix Domain Socket）提供 trait 实现和辅助功能，使 Unix 套接字能够与 Tokio 的异步运行时无缝集成。通过实现 `Listener` trait，它为 Unix 套接字监听器提供了统一的接口，支持异步接受连接和地址查询功能。

## 核心组件  
### 1. `Listener` Trait 实现  
为 `tokio::net::UnixListener` 实现了 `Listener` trait，定义了以下关键内容：  
- **关联类型**  
  - `Io`: 定义连接的 I/O 类型为 `tokio::net::UnixStream`  
  - `Addr`: 定义地址类型为 `tokio::net::unix::SocketAddr`  

- **方法实现**  
  - `poll_accept`: 通过 Tokio 的异步 `poll_accept` 方法实现连接的异步接受，返回 `(UnixStream, SocketAddr)`  
  - `local_addr`: 获取本地绑定地址，通过类型转换适配返回值  

### 2. 异步集成  
通过 `std::task::{Context, Poll}` 的使用，确保方法符合 Tokio 的异步任务轮询机制，支持在异步上下文中高效处理连接请求。

## 项目中的角色  
该文件是 Tokio 工具库（tokio-util）中网络模块的一部分，专门处理 Unix 域套接字的抽象。它通过统一的 `Listener` 接口，将 Unix 套接字与 TCP/UDP 等其他网络协议的实现整合，使项目能够以一致的方式处理不同类型的网络连接。这一设计简化了异步服务器的实现，允许开发者在不修改核心逻辑的情况下切换网络协议类型。

### 该文件在项目中的作用  